import chess

from chess_ai import move


def test_next_move():
    b = chess.Board()
    best_move = move.next_move(1, b)
    assert "a2a4" == best_move.uci()
