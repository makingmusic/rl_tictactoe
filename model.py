# this file will contain the model for the tic-tac-toe game
from itertools import product
import random
from display import GameDisplay, format_grid
from config import TIC_TAC_TOE_SIZE, GAME_WINNER_DRAW, PLAYER_X, PLAYER_O


class TicTacToeModel:
    id2board = []
    board2id = {}
    CELL_COMBINATIONS = []
    stats = []
    totalCellsOnBoard = TIC_TAC_TOE_SIZE * TIC_TAC_TOE_SIZE
    isRandomStats = False

    def __init__(self):
        self.id2board = []
        self.board2id = {}
        self.CELL_COMBINATIONS = ["X", "O", "_"]
        self.buildBoardStringIdMappings()
        self.totalCellsOnBoard = TIC_TAC_TOE_SIZE * TIC_TAC_TOE_SIZE
        self.init_stats()

    def init_stats(self):
        if self.isRandomStats:
            self.init_stats_random()
        else:
            self.init_stats_zero()
        return

    def init_stats_random(self):
        """
        Initialize stats with random values for all possible board states.
        IMPORTANT: Stats are now split by whose turn it is
        """
        total_possible_boards = len(self.id2board)
        # set the stats for the board id based on the random numbers
        # IMPORTANT: Stats are now split by whose turn it is
        self.stats = [
            {
                "X": {  # Stats when it's X's turn to move
                    "wins": [round(random.random(), 2) for _ in range(9)],
                    "losses": [round(random.random(), 2) for _ in range(9)],
                    "draws": [round(random.random(), 2) for _ in range(9)],
                    "tries": [round(random.random(), 2) for _ in range(9)],
                    "totals": {
                        "wins_X": [round(random.random(), 2) for _ in range(9)],
                        "wins_O": [round(random.random(), 2) for _ in range(9)],
                        "draws": [round(random.random(), 2) for _ in range(9)],
                    },
                },
                "O": {  # Stats when it's O's turn to move
                    "wins": [round(random.random(), 2) for _ in range(9)],
                    "losses": [round(random.random(), 2) for _ in range(9)],
                    "draws": [round(random.random(), 2) for _ in range(9)],
                    "tries": [round(random.random(), 2) for _ in range(9)],
                    "totals": {
                        "wins_X": [round(random.random(), 2) for _ in range(9)],
                        "wins_O": [round(random.random(), 2) for _ in range(9)],
                        "draws": [round(random.random(), 2) for _ in range(9)],
                    },
                },
            }
            for _ in range(total_possible_boards)
        ]

    def init_stats_zero(self):
        """
        Initialize stats with zero values for all possible board states (as if no games have been played).
        IMPORTANT: Stats are now split by whose turn it is
        """
        # Initialize stats for all possible board states, not just the number of cells
        # IMPORTANT: Stats are now split by whose turn it is
        total_possible_boards = len(self.id2board)
        self.stats = [
            {
                "X": {  # Stats when it's X's turn to move
                    "wins": [0] * 9,
                    "losses": [0] * 9,
                    "draws": [0] * 9,
                    "tries": [0] * 9,
                    "totals": {
                        "wins_X": [0] * 9,
                        "wins_O": [0] * 9,
                        "draws": [0] * 9,
                    },
                },
                "O": {  # Stats when it's O's turn to move
                    "wins": [0] * 9,
                    "losses": [0] * 9,
                    "draws": [0] * 9,
                    "tries": [0] * 9,
                    "totals": {
                        "wins_X": [0] * 9,
                        "wins_O": [0] * 9,
                        "draws": [0] * 9,
                    },
                },
            }
            for _ in range(total_possible_boards)
        ]

    def getStatsForBoardId(self, board_id, whose_turn):
        """
        Get the stats for a specific board state and player turn.

        Args:
            board_id: the id of the board
            whose_turn: "X" or "O" - whose turn it is to move
        Returns:
            Dictionary containing stats arrays for the specified player's turn
        """
        if whose_turn not in ["X", "O"]:
            raise ValueError(f"whose_turn must be 'X' or 'O', got: {whose_turn}")
        return self.stats[board_id][whose_turn]

    def getPrintableStatsForBoardIdForBothPlayers(self, board_id):
        """
        Get printable stats for a specific board state for both players.
        Formats stats side by side to save space, with X stats on top and O stats below.
        Each stat type (Wins, Losses, Draws, Tries) is displayed as a 3x3 grid.
        """
        stats_X = self.getStatsForBoardId(board_id, PLAYER_X)
        stats_O = self.getStatsForBoardId(board_id, PLAYER_O)

        size = TIC_TAC_TOE_SIZE

        def format_stat_grid(stats_dict, label):
            """Helper function to format a single stat type as a 3x3 grid."""
            values_float = [v for v in stats_dict.get(label, [])]
            values = [str(round(v, 2)) for v in values_float]
            if len(values) < size * size:
                values = list(values) + ["0"] * (size * size - len(values))
            width = max(1, max((len(str(v)) for v in values), default=1))
            rows = []
            for row_idx in range(size):
                start = row_idx * size
                row = values[start : start + size]
                rows.append(" ".join(str(v).rjust(width) for v in row))
            return rows

        # Format all stat types for both players
        x_grids = {}
        o_grids = {}
        for label in ("wins", "losses", "draws", "tries"):
            x_grids[label] = format_stat_grid(stats_X, label)
            o_grids[label] = format_stat_grid(stats_O, label)

        # Calculate column widths for alignment
        label_widths = {}
        for label in ("wins", "losses", "draws", "tries"):
            # Find the maximum width needed for this stat type across both players
            max_width = 0
            for row in x_grids[label] + o_grids[label]:
                max_width = max(max_width, len(row))
            label_widths[label] = max_width

        # Build the output string
        lines = []

        # X Player section - all stat types side by side
        lines.append("X Player:")
        # Header row with labels
        header_parts = []
        for label in ("wins", "losses", "draws", "tries"):
            header_parts.append(f"{label.capitalize():<{label_widths[label]}}")
        lines.append("  " + " | ".join(header_parts))

        # Data rows for X
        for row_idx in range(size):
            row_parts = []
            for label in ("wins", "losses", "draws", "tries"):
                row_parts.append(f"{x_grids[label][row_idx]:<{label_widths[label]}}")
            lines.append("  " + " | ".join(row_parts))

        lines.append("")  # Empty line between X and O

        # O Player section - all stat types side by side
        lines.append("O Player:")
        # Header row with labels
        header_parts = []
        for label in ("wins", "losses", "draws", "tries"):
            header_parts.append(f"{label.capitalize():<{label_widths[label]}}")
        lines.append("  " + " | ".join(header_parts))

        # Data rows for O
        for row_idx in range(size):
            row_parts = []
            for label in ("wins", "losses", "draws", "tries"):
                row_parts.append(f"{o_grids[label][row_idx]:<{label_widths[label]}}")
            lines.append("  " + " | ".join(row_parts))

        return_string = "\n".join(lines)
        return return_string

    def getPrintableStatsForBoardId(self, board_id, whose_turn):
        """
        Get printable stats for a specific board state and player turn.

        Args:
            board_id: the id of the board
            whose_turn: "X" or "O" - whose turn it is to move
        Returns:
            Formatted string representation of the stats
        """
        stats = self.getStatsForBoardId(board_id, whose_turn)
        return self.getPrintableStatsFromBoardString(stats)

    def getPrintableStatsFromBoardString(self, stats):
        size = TIC_TAC_TOE_SIZE
        sections = []
        for label in ("wins", "losses", "draws", "tries"):
            values_float = [v for v in stats.get(label, [])]
            values = [str(round(v, 2)) for v in values_float]
            if len(values) < size * size:
                values = list(values) + [0] * (size * size - len(values))
            width = max(1, max((len(str(v)) for v in values), default=1))
            rows = []
            for row_idx in range(size):
                start = row_idx * size
                row = values[start : start + size]
                rows.append(" ".join(str(v).rjust(width) for v in row))
            sections.append(f"{label.capitalize()}:\n   " + "\n   ".join(rows))

        return "\n\n".join(sections)

    def getStatsForBoardMove(self, board_id, move, whose_turn):
        """
        Get the stats for a specific move on a specific board and player turn.
        This format for the Move is going to help in the training process.

        Args:
            board_id: the id of the board
            move: the move to get the stats for
            whose_turn: "X" or "O" - whose turn it is to move
        Returns:
            a dictionary containing the stats for the move
            sample format for the move stats:
            {
                "wins": 0.5,
                "losses": 0.3,
                "draws": 0.2,
                "tries": 10,
                "totals": {
                    "wins_X": 0.5,
                    "wins_O": 0.3,
                    "draws": 0.2,
                },
            }
        """
        board_id_stats = self.getStatsForBoardId(board_id, whose_turn)
        move_stats = {}
        move_stats["wins"] = board_id_stats["wins"][move]
        move_stats["losses"] = board_id_stats["losses"][move]
        move_stats["draws"] = board_id_stats["draws"][move]
        move_stats["tries"] = board_id_stats["tries"][move]
        move_stats["totals"] = {}
        move_stats["totals"]["wins_X"] = board_id_stats["totals"]["wins_X"][move]
        move_stats["totals"]["wins_O"] = board_id_stats["totals"]["wins_O"][move]
        move_stats["totals"]["draws"] = board_id_stats["totals"]["draws"][move]
        return move_stats

    def getPrintableStatsForBoardMove(self, board_id, move, whose_turn):
        """
        Get printable stats for a specific move on a specific board and player turn.

        Args:
            board_id: the id of the board
            move: the move to get the stats for
            whose_turn: "X" or "O" - whose turn it is to move
        Returns:
            Formatted string representation of the move stats
        """
        move_stats = self.getStatsForBoardMove(board_id, move, whose_turn)
        move_win_stats = move_stats["wins"]
        move_loss_stats = move_stats["losses"]
        move_draw_stats = move_stats["draws"]
        move_tries_stats = move_stats["tries"]
        move_totals_stats = move_stats["totals"]
        # The variable type for move_totals_str_XWins is float when stats are for a single move
        move_totals_str_XWins = move_totals_stats["wins_X"]  # type: float
        move_totals_str_OWins = move_totals_stats["wins_O"]
        move_totals_str_Draws = move_totals_stats["draws"]

        str = (
            f"move {move}: on board {board_id} (Player {whose_turn}'s turn)\n"
            f"  {move_win_stats} wins\n"
            f"  {move_loss_stats} losses\n"
            f"  {move_draw_stats} draws\n"
            f"  {move_tries_stats} tries\n"
            "  Move totals:\n"
            f"    {move_totals_str_XWins} X wins\n"
            f"    {move_totals_str_OWins} O wins\n"
            f"    {move_totals_str_Draws} draws\n"
        )

        return str

    def getPrintableBoardFromId(self, board_id):
        board_string = self.id2board[board_id]
        str = self.getPrintableBoardFromString(board_string)
        return str

    def getPrintableBoardFromString(self, board_string):
        size = TIC_TAC_TOE_SIZE
        board = [[board_string[i * size + j] for j in range(size)] for i in range(size)]
        # Build the formatted board string with row and column indices as in display.py
        board_lines = []
        board_lines.append("")
        # add a line of dashes to separate the header from the board
        board_lines.append("   " + "-" * 12)
        for i, row in enumerate(board):
            row_display = f"{i} | " + " | ".join(row) + " |"
            board_lines.append(row_display)
            board_lines.append("   " + "-" * 12)
        # Add column numbers
        col_numbers = "   " + "   ".join([str(i) for i in range(size)])
        board_lines.append(" " + col_numbers)
        return "\n".join(board_lines)

    def buildBoardStringIdMappings(self):
        # reset the mappings if they exist
        self.board2id = {}
        self.id2board = []

        # Enumerate in a fixed order so it's reproducible and can be used for indexing.
        for digits in product(self.CELL_COMBINATIONS, repeat=9):
            s = "".join(digits)  # e.g., "_X_O_____"
            self.board2id[s] = len(self.id2board)
            self.id2board.append(s)

    def setMoveStatsForBoardId(self, board_id, move, whose_turn, who_won):
        """
        Set the stats for a specific move on a specific board and player turn.
        This function is only useful for state updates for one board state.
        A separate function should be used to update the stats for all board states. (using history)

        The function determines win/loss/draw from the perspective of the player whose turn it is:
        - If who_won == whose_turn: This move led to a win for the current player
        - If who_won != whose_turn (and not a draw): This move led to a loss for the current player
        - If who_won is GAME_WINNER_DRAW or None: This move led to a draw

        Stats are only updated for the player making the move (whose_turn).

        For reference, Sample stats format:
        stats[board_id] = {
            "X": {  # When it's X's turn
                "wins": [0.5, 0.3, 0.2, ...],
                "losses": [0.3, 0.2, 0.1, ...],
                "draws": [0.2, 0.1, 0.0, ...],
                "tries": [10, 10, 10, ...],
                "totals": {
                    "wins_X": [0.5, 0.3, 0.2, ...],
                    "wins_O": [0.3, 0.2, 0.1, ...],
                    "draws": [0.2, 0.1, 0.0, ...],
                },
            },
            "O": {  # When it's O's turn
                "wins": [0.5, 0.3, 0.2, ...],
                "losses": [0.3, 0.2, 0.1, ...],
                "draws": [0.2, 0.1, 0.0, ...],
                "tries": [10, 10, 10, ...],
                "totals": {
                    "wins_X": [0.5, 0.3, 0.2, ...],
                    "wins_O": [0.3, 0.2, 0.1, ...],
                    "draws": [0.2, 0.1, 0.0, ...],
                },
            },
        }

        Args:
            board_id: the id of the board
            move: the move to set the stats for
            whose_turn: "X" or "O" - whose turn it is to move (the player making this move)
            who_won: the winner of the game (PLAYER_X, PLAYER_O, or GAME_WINNER_DRAW/None for draw)
        """
        # Validate whose_turn parameter
        if whose_turn not in [PLAYER_X, PLAYER_O]:
            raise ValueError(
                f"Invalid whose_turn value: {whose_turn}. Expected PLAYER_X or PLAYER_O"
            )

        # Validate who_won parameter
        if who_won not in [PLAYER_X, PLAYER_O, GAME_WINNER_DRAW, None]:
            raise ValueError(
                f"Invalid who_won value: {who_won}. Expected PLAYER_X, PLAYER_O, GAME_WINNER_DRAW, or None"
            )

        # Determine win/loss/draw from the perspective of whose_turn
        # explanation:
        # - is_draw: the game ended in a draw
        # - is_win_for_whose_turn: the game ended in a win for whose_turn (whose_turn won)
        # - is_loss_for_whose_turn: the game ended in a loss for whose_turn (whose_turn lost)
        is_draw = who_won == GAME_WINNER_DRAW or who_won is None
        is_win_for_whose_turn = not is_draw and who_won == whose_turn
        is_loss_for_whose_turn = not is_draw and who_won != whose_turn

        # getStatsForBoardId returns stats[board_id][whose_turn]
        stats_to_update = self.getStatsForBoardId(board_id, whose_turn)

        # Always increment tries for this move
        stats_to_update["tries"][move] += 1

        if is_win_for_whose_turn:
            # This move by whose_turn led to a win for whose_turn
            stats_to_update["wins"][move] += 1
            if whose_turn == PLAYER_X:
                stats_to_update["totals"]["wins_X"][move] += 1
            else:  # whose_turn == PLAYER_O
                stats_to_update["totals"]["wins_O"][move] += 1

        elif is_loss_for_whose_turn:
            # This move by whose_turn led to a loss for whose_turn (opponent won)
            stats_to_update["losses"][move] += 1
            if whose_turn == PLAYER_X:
                # X lost, so O won
                stats_to_update["totals"]["wins_O"][move] += 1
            else:  # whose_turn == PLAYER_O
                # O lost, so X won
                stats_to_update["totals"]["wins_X"][move] += 1

        elif is_draw:
            # This move led to a draw
            stats_to_update["draws"][move] += 1
            stats_to_update["totals"]["draws"][move] += 1

        self.stats[board_id][whose_turn] = stats_to_update
        return

    def setMoveStatsForEntireGameFromHistory(self, history, who_won):
        """
        Set the stats for an entire game.
        * history will contain a list containing tuples of
        ** board_id (board state)
        ** move (the move made - index of the move)
        ** who_moved (the player who made the move)
        * who_won (the player who won the game) : separate variable.
          Can be PLAYER_X, PLAYER_O, or GAME_WINNER_DRAW/None for a draw.

        Sample history format:
        [
            (board_id, move, who_moved),
            (board_id, move, who_moved),
            ...
        ]

        Example history:
        [
            (2180, 0, "X"), (2180, 1, "O"), (2180, 2, "X"),
            (2180, 3, "O"), (2180, 4, "X"), (2180, 5, "O"),
            (2180, 6, "X"), (2180, 7, "O"), (2180, 8, "X"),
            ...
        ]

        Args:
            history: a list of moves (follows the structure described above)
            who_won: the winner of the game (PLAYER_X, PLAYER_O, or GAME_WINNER_DRAW/None for draw)
        """
        # Handle empty history
        if not history:
            return  # Empty history, nothing to update

        # verify that who_won is a valid value
        if who_won not in [PLAYER_X, PLAYER_O, GAME_WINNER_DRAW, None]:
            raise ValueError(
                f"Invalid who_won value: {who_won}. Expected PLAYER_X, PLAYER_O, GAME_WINNER_DRAW, or None"
            )

        # Cycle through history and update stats for each move
        for board_id, move, who_moved in history:
            self.setMoveStatsForBoardId(board_id, move, who_moved, who_won)
        return


# move all test functionality in to a separate function.
# need not be part of the class.
def test_TicTacToeModel():
    model = TicTacToeModel()

    # Tesitng if board move stats update properly
    # Create a test history and set the stats for the entire game using the history
    # start with a blank board
    test_board_string_0 = "_________"
    test_board_string_1 = "X________"
    test_board_string_2 = "XO_______"
    test_board_string_3 = "XO_X_____"
    test_board_string_4 = "XO_XO____"
    test_board_string_5 = "XO_XO_X__"

    test_board_id_0 = model.board2id[test_board_string_0]
    test_board_id_1 = model.board2id[test_board_string_1]
    test_board_id_2 = model.board2id[test_board_string_2]
    test_board_id_3 = model.board2id[test_board_string_3]
    test_board_id_4 = model.board2id[test_board_string_4]
    test_board_id_5 = model.board2id[test_board_string_5]  # X wins here.

    test_history = []
    test_history = [
        (test_board_id_0, 0, PLAYER_X),
        (test_board_id_1, 1, PLAYER_O),
        (test_board_id_2, 3, PLAYER_X),
        (test_board_id_3, 4, PLAYER_O),
        (test_board_id_4, 6, PLAYER_X),
    ]

    # for each board in the history, print the stats for the board
    print("--------------------------------")
    print("Printing stats for each board in the history")
    print("--------------------------------")
    for board_id, move, who_moved in test_history:
        print(f"Board {board_id} with {move} by {who_moved} and all stats")
        print(model.getPrintableBoardFromId(board_id))
        print(model.getPrintableStatsForBoardIdForBothPlayers(board_id))
        print("--------------------------------")

    print("--------------------------------")
    print("Testing One Shot update based on history list")
    print("--------------------------------")
    # now do the same thing in one shot using the history function.
    # first print the board_id_0 stats before
    print("BEFORE STATS FOR ALL BOARDS")
    print(model.getPrintableBoardFromId(test_board_id_0))
    print(model.getPrintableStatsForBoardIdForBothPlayers(test_board_id_0))
    print("----")
    print(model.getPrintableBoardFromId(test_board_id_1))
    print(model.getPrintableStatsForBoardIdForBothPlayers(test_board_id_1))
    print("----")
    print(model.getPrintableBoardFromId(test_board_id_2))
    print(model.getPrintableStatsForBoardIdForBothPlayers(test_board_id_2))
    print("----")
    print(model.getPrintableBoardFromId(test_board_id_3))
    print(model.getPrintableStatsForBoardIdForBothPlayers(test_board_id_3))
    print("----")
    print(model.getPrintableBoardFromId(test_board_id_4))
    print(model.getPrintableStatsForBoardIdForBothPlayers(test_board_id_4))

    # update stats using history function
    print("--------------------------------")
    print("NOW UPDATING STATS FOR ALL BOARDS")
    print("--------------------------------")

    model.setMoveStatsForEntireGameFromHistory(test_history, PLAYER_X)

    # print after stats
    print("AFTER STATS FOR ALL BOARDS")
    print(model.getPrintableBoardFromId(test_board_id_0))
    print(model.getPrintableStatsForBoardIdForBothPlayers(test_board_id_0))
    print("----")
    print(model.getPrintableBoardFromId(test_board_id_1))
    print(model.getPrintableStatsForBoardIdForBothPlayers(test_board_id_1))
    print("----")
    print(model.getPrintableBoardFromId(test_board_id_2))
    print(model.getPrintableStatsForBoardIdForBothPlayers(test_board_id_2))
    print("----")
    print(model.getPrintableBoardFromId(test_board_id_3))
    print(model.getPrintableStatsForBoardIdForBothPlayers(test_board_id_3))
    print("----")
    print(model.getPrintableBoardFromId(test_board_id_4))
    print(model.getPrintableStatsForBoardIdForBothPlayers(test_board_id_4))


if __name__ == "__main__":
    test_TicTacToeModel()
