from t3 import TicTacToe
from display import GameDisplay
import time as t

########################################################
# Initialize the game and display system
########################################################
game = TicTacToe()

display = GameDisplay(clear_screen=True, delay=0.1)  # 1 second delay between moves 
display.display_board(game, "Game Started - Empty Board")

########################################################
# Make moves and display each step
########################################################
moves = [
    (0, 1, "Player X moves to (0,0)"),
    (0, 2, "Player X moves to (0,2)"),
    (1, 0, "Player O moves to (1,0)"),
    (1, 1, "Player X moves to (1,1)"),
    (1, 2, "Player O moves to (1,2)"),
    (2, 0, "Player X moves to (2,0)"),
    (2, 1, "Player O moves to (2,1)"),
    (2, 2, "Player X moves to (2,2)"),
    (0, 0, "Player O moves to (0,0)")
]


move_count = 0
for row, col, move_info in moves:
    if not game.is_game_over:
        game.make_move(row, col)
        move_count += 1
        
        # Determine game state info
        game_info = None
        if game.is_game_over:
            if game.winner == 'X':
                game_info = "🎉 X Wins!"
            elif game.winner == 'O':
                game_info = "🎉 O Wins!"
            elif game.winner == 'NOBODY WON':
                game_info = "🤝 It's a Draw!"
        
        display.display_board(game, move_info, game_info)
    else:
        print ("Game is over. Stopping. The winner is: ", game.winner)
        break

########################################################
# Display final game summary
########################################################
display.display_game_summary(game, move_count)

