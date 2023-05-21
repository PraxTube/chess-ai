import chess_ai.chess_engine as chess

from chess_ai import move


def test_next_move():
    b = chess.Board()
    legal_moves = b.legal_moves()
    best_move = move.next_move(1, b)
    assert best_move in legal_moves
