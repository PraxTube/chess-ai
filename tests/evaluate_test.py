import chess

from chess_ai import evaluate


def test_evaluate_board():
    b = chess.Board()
    value = evaluate.evaluate_board(b)
    assert 0 == value

    b = chess.Board("4kr2/4b3/8/2p1R2p/4n1p1/3q2P1/7P/4K3 w - - 4 38")
    value = evaluate.evaluate_board(b)
    assert -16 == value
    value = evaluate.evaluate_board(b, chess.Move.from_uci("e5h5"))
    assert -15 == value

    b = chess.Board("4kr2/4b3/8/2p1R2p/4n1p1/3q2P1/7P/8")
    value = evaluate.evaluate_board(b)
    assert -916 == value
