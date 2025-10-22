"""
Display module for Tic-Tac-Toe game visualization.
Provides clean board display with in-place updates for reinforcement learning visualization.
"""

import os
import sys
import time
from typing import Optional


class GameDisplay:
    """Handles the display of the tic-tac-toe board with in-place updates."""

    def __init__(self, clear_screen: bool = True, delay: float = 0.5):
        """
        Initialize the display system.

        Args:
            clear_screen: Whether to clear the screen between updates
            delay: Delay in seconds between board updates (for visualization)
        """
        self.clear_screen = clear_screen
        self.delay = delay
        self.first_display = True

    def clear_terminal(self):
        """Clear the terminal screen."""
        if self.clear_screen:
            os.system("cls" if os.name == "nt" else "clear")

    def display_board(
        self,
        game,
        move_info: Optional[str] = None,
        game_info: Optional[str] = None,
        clear_screen: bool = False,
    ):
        """
        Display the current board state with optional move and game information.

        Args:
            game: TicTacToe game instance
            move_info: Information about the current move (e.g., "Player X moves to (1,1)")
            game_info: Information about game state (e.g., "Game Over - X Wins!")
        """

        # Clear screen if not the first display
        if clear_screen:
            self.clear_terminal()

        # Display header information
        if move_info:
            print(f"🎯 {move_info}")
            print("-" * 30)

        # Display the board
        print("Current Board:")
        for i, row in enumerate(game.board):
            # Add row numbers for better visualization
            row_display = f"{i} | " + " | ".join(row) + " |"
            print(row_display)

        # Add column numbers
        col_numbers = "   " + "   ".join([str(i) for i in range(len(game.board[0]))])
        print("   " + "-" * (len(col_numbers)))
        print(" " + col_numbers)

        # Display game state information
        if game_info:
            print(f"\n🎮 {game_info}")

        # Display current player and game status
        if not game.is_game_over:
            print(f"👤 Next Player: {game.next_player}")
        else:
            if game.winner == "X":
                print("🏆 Winner: X")
            elif game.winner == "O":
                print("🏆 Winner: O")
            elif game.winner == "NOBODY WON":
                print("🤝 It's a Draw!")

        print("\n" + "=" * 30)

        # Add delay for visualization
        if self.delay > 0:
            time.sleep(self.delay)

        self.first_display = False

    def display_game_summary(self, game, total_moves: int = None):
        # Game results:
        winner_string = (
            "X" if game.winner == "X" else "O" if game.winner == "O" else "NOBODY"
        )
        # identify the value of total_moves from the game object itself.
        if total_moves is None:
            total_moves = game.move_count

        print(f"\n {winner_string} wins in {total_moves} moves.")
        print("\n" + "=" * 30)
