from evaluate import evaluate_board
import chess_engine as chess

board = chess.Board(fen_board="8/1n1PB1p1/R2P1q2/p2P3P/1PN1P2k/2R5/N1p2r1P/1b4K1 w - - 0 1")

a = evaluate_board(board)

print(a)

