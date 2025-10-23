# will instatiate a game of TicTacToe and it can be played by a human against the computer
# to begin with, the computer will only chose random moves
from t3 import TicTacToe
from moves import TicTacToeMoves
from display import GameDisplay

display = GameDisplay(clear_screen=True, delay=0.1)  # 0.1 second delay between moves
game = TicTacToe()

print(
    "Welcome to TicTacToe! You are playing against the computer. You are X and the computer is O."
)

while not game.is_game_over:
    display.display_board(game, clear_screen=True)
    move = input("Enter your move (row, col) or 'q' to quit: ")
    if move == "q":
        break
    row, col = move.split(",")
    game.make_move(int(row), int(col))
    computer_move = TicTacToeMoves().generate_random_move(game)
    game.make_move(computer_move[0], computer_move[1])
    display.display_board(game, clear_screen=True)
    if game.is_game_over:
        break

display.display_game_summary(game)
print("Game over! Thanks for playing.")
