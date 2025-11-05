## Tic-Tac-Toe stats data structures

This project maintains per-board and per-move statistics to support learning and analysis. The core structures live in `model.py` within `TicTacToeModel`.

### Board and move addressing
- **Board identity**: Each board state is a 9-character string over `{"X","O","_"}`. Two mappings are maintained:
  - `board2id: dict[str, int]` maps a board string to a numeric `board_id`.
  - `id2board: list[str]` maps a numeric `board_id` back to the board string.
- **Move index**: A move is an integer in `[0, 8]`, indexing cells row-major on a 3×3 grid.

### Per-board stats store (`stats[board_id]`)
For each `board_id`, `stats[board_id]` is a dictionary with keys `"X"` and `"O"` representing whose turn it is to move. Each player's stats contains arrays aligned by `move` index (0–8):

```json
{
  "X": {  // Stats when it's X's turn to move
    "wins":   [number, number, ..., number],   // length 9
    "losses": [number, number, ..., number],   // length 9
    "draws":  [number, number, ..., number],   // length 9
    "tries":  [number, number, ..., number],   // length 9
    "totals": {
      "wins_X": [number, number, ..., number], // length 9
      "wins_O": [number, number, ..., number], // length 9
      "draws":  [number, number, ..., number]  // length 9
    }
  },
  "O": {  // Stats when it's O's turn to move
    "wins":   [number, number, ..., number],   // length 9
    "losses": [number, number, ..., number],   // length 9
    "draws":  [number, number, ..., number],   // length 9
    "tries":  [number, number, ..., number],   // length 9
    "totals": {
      "wins_X": [number, number, ..., number], // length 9
      "wins_O": [number, number, ..., number], // length 9
      "draws":  [number, number, ..., number]  // length 9
    }
  }
}
```

**IMPORTANT**: The stats are separated by whose turn it is because:
- The same board state can have different optimal moves depending on which player is moving
- "Wins" and "losses" are from the perspective of the current player (whose turn it is)
- Without this separation, the model would mix statistics from both players' perspectives and fail to learn properly

Semantics per move index:
- **wins**: Proportion or score of games won (from the current player's perspective) when this move was played from this board.
- **losses**: Proportion or score of games lost when this move was played.
- **draws**: Proportion or score of draws when this move was played.
- **tries**: Number of times this move has been tried from this board (can be non-integer if normalized/averaged during initialization or training).
- **totals.wins_X / wins_O / draws**: Outcome rates split by final winner (X, O) or draw when this move was played from this board.

Notes:
- Initialization may seed these arrays with random floating-point values for experimentation; training should update them to reflect actual outcomes.
- Cells corresponding to illegal moves (occupied cells) can remain at zero or be ignored by the policy.
- To determine whose turn it is from a board string: count X's and O's. If equal, it's X's turn; if X count is one more, it's O's turn.

### Per-move serializer (`getStatsForBoardMove`)
The function `getStatsForBoardMove(board_id, move, whose_turn)` extracts a single-move view (a "serializer") from the per-board store:

```json
{
  "wins":   number,
  "losses": number,
  "draws":  number,
  "tries":  number,
  "totals": {
    "wins_X": number,
    "wins_O": number,
    "draws":  number
  }
}
```

This object is derived by indexing each per-board array at `move` for the specified player's turn. For example:
- `wins` is `stats[board_id][whose_turn]["wins"][move]`.
- `totals.wins_X` is `stats[board_id][whose_turn]["totals"]["wins_X"][move]`.

The `whose_turn` parameter is required and must be either `"X"` or `"O"`.

### Update lifecycle
After each completed game, the training loop should update `stats[board_id][whose_turn]` for the moves taken during the game, incrementing `tries` and adjusting `wins`, `losses`, `draws`, and `totals` for the observed outcome. The serializer provides the per-move snapshot commonly needed for decision-making, display, or logging.

**Important**: When updating stats after a game, make sure to use the correct `whose_turn` value for each move. This ensures that X's moves update X's stats and O's moves update O's stats.

### Examples: two snapshots of the stats data structure within @model.py 
Below are two realistic examples that might help.


#### Example A: Early-game snapshot (empty board, exploratory initialization)
Context:
- `board_string`: `"_________"` (all cells empty)
- `board_id`: some integer mapped from `board2id["_________"]`
- Since the board is empty, X count = 0 and O count = 0, so it's X's turn
- Values are plausible randomized seeds prior to training updates

```json
{
  "X": {  // Stats when it's X's turn to move
    "wins":   [0.51, 0.47, 0.55, 0.49, 0.52, 0.46, 0.50, 0.53, 0.48],
    "losses": [0.31, 0.36, 0.29, 0.33, 0.30, 0.35, 0.34, 0.28, 0.37],
    "draws":  [0.18, 0.17, 0.16, 0.18, 0.18, 0.19, 0.16, 0.19, 0.15],
    "tries":  [0.92, 1.05, 0.87, 0.99, 1.10, 0.95, 0.90, 1.02, 0.88],
    "totals": {
      "wins_X": [0.28, 0.25, 0.30, 0.26, 0.29, 0.24, 0.27, 0.31, 0.23],
      "wins_O": [0.23, 0.22, 0.25, 0.23, 0.23, 0.22, 0.23, 0.22, 0.24],
      "draws":  [0.18, 0.17, 0.16, 0.18, 0.18, 0.19, 0.16, 0.19, 0.15]
    }
  },
  "O": {  // Stats when it's O's turn to move (less relevant for empty board but included)
    "wins":   [0.48, 0.52, 0.49, 0.51, 0.47, 0.53, 0.50, 0.46, 0.54],
    "losses": [0.35, 0.31, 0.34, 0.32, 0.36, 0.30, 0.33, 0.37, 0.29],
    "draws":  [0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.16, 0.17],
    "tries":  [0.88, 0.95, 0.91, 0.93, 0.89, 0.97, 0.92, 0.86, 0.99],
    "totals": {
      "wins_X": [0.24, 0.27, 0.25, 0.26, 0.23, 0.28, 0.25, 0.22, 0.29],
      "wins_O": [0.24, 0.25, 0.24, 0.25, 0.24, 0.25, 0.25, 0.24, 0.25],
      "draws":  [0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.16, 0.17]
    }
  }
}
```

Notes:
- Each array is length 9 and aligned by move index `[0..8]`.
- Cells corresponding to illegal moves would remain 0.0; on an empty board all moves are legal.
- The stats are separated by whose turn it is, enabling proper learning for each player.

#### Example B: Mid-game snapshot (board with occupied cells)
Context:
- `board_string`: `"X_O__X___"` (row-major; indices 0..8)
- Occupied indices: 0 = `X`, 2 = `O`, 5 = `X`
- X count = 2, O count = 1, so it's O's turn
- Illegal move slots show zeros across arrays

```json
{
  "X": {  // Stats when it's X's turn to move
    "wins":   [0.00, 0.61, 0.00, 0.64, 0.58, 0.00, 0.62, 0.52, 0.60],
    "losses": [0.00, 0.20, 0.00, 0.18, 0.23, 0.00, 0.16, 0.26, 0.19],
    "draws":  [0.00, 0.19, 0.00, 0.18, 0.19, 0.00, 0.22, 0.22, 0.21],
    "tries":  [0.00, 7.00, 0.00, 8.00, 6.00, 0.00, 5.00, 4.00, 5.00],
    "totals": {
      "wins_X": [0.00, 0.37, 0.00, 0.40, 0.36, 0.00, 0.38, 0.32, 0.35],
      "wins_O": [0.00, 0.24, 0.00, 0.24, 0.22, 0.00, 0.24, 0.20, 0.25],
      "draws":  [0.00, 0.19, 0.00, 0.18, 0.19, 0.00, 0.22, 0.22, 0.21]
    }
  },
  "O": {  // Stats when it's O's turn to move (relevant for this board state)
    "wins":   [0.00, 0.58, 0.00, 0.62, 0.55, 0.00, 0.60, 0.49, 0.57],
    "losses": [0.00, 0.22, 0.00, 0.20, 0.25, 0.00, 0.18, 0.28, 0.21],
    "draws":  [0.00, 0.20, 0.00, 0.18, 0.20, 0.00, 0.22, 0.23, 0.22],
    "tries":  [0.00, 8.00, 0.00, 9.00, 7.00, 0.00, 6.00, 5.00, 6.00],
    "totals": {
      "wins_X": [0.00, 0.35, 0.00, 0.38, 0.34, 0.00, 0.36, 0.30, 0.33],
      "wins_O": [0.00, 0.23, 0.00, 0.24, 0.21, 0.00, 0.24, 0.19, 0.24],
      "draws":  [0.00, 0.20, 0.00, 0.18, 0.20, 0.00, 0.22, 0.23, 0.22]
    }
  }
}
```

Notes:
- Indices 0, 2, and 5 (already occupied) are zeroed, reflecting illegal moves.
- `tries` are integer-like here to illustrate post-game updates; other arrays remain floating-point ratios.
- For this board state (X count = 2, O count = 1), it's O's turn to move, so the O stats are more relevant.
- Both X and O stats are maintained because the same board configuration could theoretically be reached in different game orders.
