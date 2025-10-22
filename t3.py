# This is a Tic-Tac-Toe environment class.
# You can initilize it with an empty game
# Instantiate this class to create an empty game state

STRING_X = "X"
STRING_O = "O"
STRING_EMPTY = "_"
STRING_DELIMITER = " "

STRING_WINNER_DRAW = "DRAW"
STRING_WINNER_NONE = "NOBODY WON"


class WrongMoveError(Exception):
    def __init__(self, message):
        print(f"[LOG]: WrongMoveError raised: {message}")
        super().__init__(message)


class TicTacToe:
    # init function that will create the following attributes.
    def __init__(self, size=3):
        # board size:
        self.size = size
        # board:
        # - A good data structure to store the tictactoe board is a 2D list (list of lists), where each element represents a cell on the board.
        #   A string representation of the board can be created by joining the elements of the 2D list with a delimiter.
        self.board = [[STRING_EMPTY] * size for _ in range(size)]
        # next player:
        self.next_player = STRING_X
        # winner:
        self.winner = None  # None (if game is not over), STRING_X, or STRING_O, or DRAW (if game is a draw)
        # is game over:
        self.is_game_over = False
        # open positions:
        self.open_positions = [i for i in range(size * size)]
        # move count:
        self.move_count = 0

    # print the board to the console:
    def print_board(self):
        for row in self.board:
            print(STRING_DELIMITER.join(row))
        print()

    # make a move on the board:
    # return the winner of the game or None if the game is not over
    def make_move(self, row, col, whose_turn=None):
        if self.board[row][col] != STRING_EMPTY:
            raise WrongMoveError("Cell already taken")  # custom error class

        # it is the turn of self.next_player
        if whose_turn is not None and whose_turn != self.next_player:
            raise WrongMoveError(
                f"Turn mismatch. Expected: {self.next_player}, but got: {whose_turn}"
            )

        self.board[row][col] = self.next_player
        self.open_positions.remove(row * self.size + col)

        # move the turn to the next player
        self.next_player = STRING_O if self.next_player == STRING_X else STRING_X
        # see if anybody has won the game
        self.winner = self.check_win()
        # update self.is_game_over
        self.is_game_over = self.winner is not None
        # update move count
        self.move_count += 1
        return self.winner

    def check_win(self):
        # check if the game is over:
        # first, check if there is any valid moves remaining

        # Step 1: check all rows to see if any player has won the game
        for row in self.board:
            if row.count(STRING_X) == self.size:
                return STRING_X
            if row.count(STRING_O) == self.size:
                return STRING_O
        # Step 2:then we check all columns to see if any player has won the game
        for col in range(self.size):
            if [self.board[row][col] for row in range(self.size)].count(
                STRING_X
            ) == self.size:
                return STRING_X
            if [self.board[row][col] for row in range(self.size)].count(
                STRING_O
            ) == self.size:
                return STRING_O
        # Step 3: then we check both diagonals to see if any player has won the game
        if [self.board[i][i] for i in range(self.size)].count(STRING_X) == self.size:
            return STRING_X
        if [self.board[i][i] for i in range(self.size)].count(STRING_O) == self.size:
            return STRING_O

        # if no player has won the game, return None
        return None
