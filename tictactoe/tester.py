from tictactoe import actions, X, O, EMPTY, result, player, winner,terminal, min_value, max_value

board = [[EMPTY, EMPTY, EMPTY],
        [X, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]]

print(min_value(board))
