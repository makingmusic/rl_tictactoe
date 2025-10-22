import random
from t3 import TicTacToe, STRING_X, STRING_O


class TicTacToeMoves:
    """
    A class to generate predefined and random moves for Tic-Tac-Toe testing.
    """

    def __init__(self):
        self.size = 3

    def movesForXWin(self):
        """
        Generate a predefined set of moves that results in X winning.
        Returns a list of tuples in format (row, col, description).
        """
        return [
            (0, 0, "Player X moves to (0,0)"),
            (1, 0, "Player O moves to (1,0)"),
            (0, 1, "Player X moves to (0,1)"),
            (1, 1, "Player O moves to (1,1)"),
            (0, 2, "Player X moves to (0,2)"),  # X wins with top row
        ]

    def movesForOWin(self):
        """
        Generate a predefined set of moves that results in O winning.
        Returns a list of tuples in format (row, col, description).
        """
        return [
            (0, 0, "Player X moves to (0,0)"),
            (1, 0, "Player O moves to (1,0)"),
            (0, 1, "Player X moves to (0,1)"),
            (1, 1, "Player O moves to (1,1)"),
            (2, 2, "Player X moves to (2,2)"),
            (1, 2, "Player O moves to (1,2)"),  # O wins with middle row
        ]

    def movesForDraw(self):
        """
        Generate a predefined set of moves that results in a draw.
        Returns a list of tuples in format (row, col, description).
        """
        return [
            (0, 0, "Player X moves to (0,0)"),
            (0, 1, "Player O moves to (0,1)"),
            (0, 2, "Player X moves to (0,2)"),
            (1, 1, "Player O moves to (1,1)"),
            (1, 0, "Player X moves to (1,0)"),
            (1, 2, "Player O moves to (1,2)"),
            (2, 1, "Player X moves to (2,1)"),
            (2, 0, "Player O moves to (2,0)"),
            (2, 2, "Player X moves to (2,2)"),  # Draw - no winner
        ]

    def generate_random_moves(self, max_moves=9):
        """
        Generate random legal moves for testing.

        Args:
            max_moves (int): Maximum number of moves to generate (default: 9 for full board)

        Returns:
            list: List of tuples in format (row, col, description)
        """
        game = TicTacToe()
        moves = []
        current_player = STRING_X

        # Generate random moves until game is over or max_moves reached
        for move_num in range(max_moves):
            if game.is_game_over:
                break

            # Get available positions
            available_positions = []
            for row in range(self.size):
                for col in range(self.size):
                    if game.board[row][col] == "_":
                        available_positions.append((row, col))

            if not available_positions:
                break

            # Choose a random available position
            row, col = random.choice(available_positions)

            # Create move description
            player_name = "X" if current_player == STRING_X else "O"
            description = f"Player {player_name} moves to ({row},{col})"

            # Add move to list
            moves.append((row, col, description))

            # Make the move in the game
            try:
                game.make_move(row, col)
                current_player = STRING_O if current_player == STRING_X else STRING_X
            except Exception as e:
                # This shouldn't happen with legal moves, but just in case
                print(
                    f"Error while building random moves for testing: making move: {e}"
                )
                break

        return moves

    def generate_random_move(self, game: TicTacToe):
        """
        Generate a random move for the game.
        Returns a tuple (row, col) representing the move.
        """
        # Convert linear position to row, col coordinates
        linear_pos = random.choice(game.open_positions)
        row = linear_pos // game.size
        col = linear_pos % game.size
        return (row, col)
