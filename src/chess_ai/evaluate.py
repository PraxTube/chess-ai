import numpy as np


def evaluate_board(board, move=None):
    start_fen = board.fen()

    if move:
        board.makeMove(move)
        fen_string = board.fen().split()[0]
        board.undoMove()
    else:
        fen_string = board.fen().split()[0]

    if start_fen != board.fen():
        raise ValueError(
            "The board was not properly cleaned up!", start_fen, board.fen()
        )

    piece_chars = ["p", "b", "n", "r", "q", "k"]
    white_pieces = np.array([fen_string.count(x.upper()) for x in piece_chars])
    black_pieces = np.array([fen_string.count(x) for x in piece_chars])

    multiplication_mask = np.array([1, 3, 3, 5, 9, 900])
    return white_pieces.dot(multiplication_mask) - black_pieces.dot(multiplication_mask)
