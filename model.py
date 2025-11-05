# this file will contain the model for the tic-tac-toe game
from itertools import product
import random
from display import GameDisplay, format_grid
from config import TIC_TAC_TOE_SIZE


class TicTacToeModel:
    id2board = []
    board2id = {}
    CELL_COMBINATIONS = []
    stats = []
    totalCellsOnBoard = TIC_TAC_TOE_SIZE * TIC_TAC_TOE_SIZE

    def __init__(self):
        self.id2board = []
        self.board2id = {}
        self.CELL_COMBINATIONS = ["X", "O", "_"]
        self.buildBoardStringIdMappings()
        self.totalCellsOnBoard = TIC_TAC_TOE_SIZE * TIC_TAC_TOE_SIZE
        self.init_stats()

    def init_stats(self):
        ########################################################################
        # random stats
        ########################################################################
        total_possible_boards = len(self.id2board)
        use_random = True
        if use_random:
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
            return
        ########################################################################

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

    def setMoveStatsForBoardId(self, board_id, move, whose_turn, win, loss, draw):
        """
        Set the stats for a specific move on a specific board and player turn.
        This function is only useful for board states that are at the end of a game.
        For reference,
        Sample move_stats format:
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
        Sample stats format:
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
            whose_turn: "X" or "O" - whose turn it is to move
            win: the win value to set
            loss: the loss value to set
            draw: the draw value to set
        """
        # TODO: Implement this function when needed for training
        return


if __name__ == "__main__":
    model = TicTacToeModel()
    # pick a random number from 0 to maximum possible board string index
    random_board_id = random.randint(0, len(model.id2board) - 1)

    # Get the board string to determine whose turn it is
    board_string = model.id2board[random_board_id]
    # Count X's and O's to determine whose turn it is
    x_count = board_string.count("X")
    o_count = board_string.count("O")
    # If X and O counts are equal, it's X's turn (X goes first)
    # If X count is one more than O count, it's O's turn
    whose_turn = "X" if x_count == o_count else "O"

    print("picked a random board id: ", random_board_id)
    print(f"Board string: {board_string}")
    print(f"Whose turn: {whose_turn} (X count: {x_count}, O count: {o_count})")

    print("\nprintable board:")
    printable = model.getPrintableBoardFromId(random_board_id)
    print(printable)

    print("\nprintable board stats:")
    printable_board_stats = model.getPrintableStatsForBoardId(
        random_board_id, whose_turn
    )
    print(printable_board_stats)

    print("\nrandom board move stats:")
    random_move = random.randint(0, model.totalCellsOnBoard - 1)
    stats_for_board_move = model.getPrintableStatsForBoardMove(
        random_board_id, random_move, whose_turn
    )
    print(stats_for_board_move)
