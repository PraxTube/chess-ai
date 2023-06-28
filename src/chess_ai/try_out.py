import chess_engine as chess
row, col = 7,4 
contact_squares = []

board = chess.Board().board

for i in range(row - 1, row + 2):
    for j in range(col - 1, col + 2):
        if 0 <= i < 8 and 0 <= j < 8 and (i, j) != (row, col):
            contact_squares.append((i, j))

print(contact_squares)