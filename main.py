########################################################
# import modules
# ########################################################
import time as t
from t3 import TicTacToe
from display import GameDisplay
from moves import TicTacToeMoves
from config import DELAY_BETWEEN_MOVES, CLEAR_SCREEN, TIC_TAC_TOE_SIZE

########################################################
# Initialize the game and display system
########################################################
game = TicTacToe()
display = GameDisplay(clear_screen=CLEAR_SCREEN, delay=DELAY_BETWEEN_MOVES)

########################################################
# Make moves and display each step
########################################################
moves = TicTacToeMoves().generate_random_moves(
    max_moves=TIC_TAC_TOE_SIZE * TIC_TAC_TOE_SIZE
)

move_count = 0
for row, col, move_info in moves:
    if not game.is_game_over:
        game.make_move(row, col)
        move_count += 1

        if game.is_game_over:
            game_winner = game.winner
        else:
            game_winner = "Nobody"

        display.display_board(
            game, move_info, f"The winner is: {game_winner}", clear_screen=True
        )
    else:
        print("Game is over. Stopping. The winner is: ", game.winner)
        break

########################################################
# Display final game summary
########################################################
display.display_game_summary(game, move_count)
