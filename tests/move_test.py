import chess

from chess_ai import move


def test_next_move():
    b = chess.Board()
    best_move = move.next_move(1, b)
    assert "a2a4" == best_move.uci()


def test_get_ordered_moves():
    b = chess.Board("4kr2/4b3/8/2p1R2p/4n1p1/3q2P1/7P/4K3 w - - 4 38")
    actual_ordered_moves = move.get_ordered_moves(b)
    expected_ordered_moves = [
        "e5e7",
        "e5e4",
        "e5h5",
        "e5c5",
        "e5e6",
        "e5g5",
        "e5f5",
        "e5d5",
        "h2h3",
        "h2h4",
    ]

    assert len(expected_ordered_moves) == len(actual_ordered_moves)

    for i in range(len(expected_ordered_moves)):
        assert expected_ordered_moves[i] == actual_ordered_moves[i].uci()


def test_minimax_root():
    b = chess.Board()
    best_move = move.minimax_root(1, b)
    assert "a2a4" == best_move.uci()

    b = chess.Board("4kr2/4b3/8/2p1R2p/4n1p1/3q2P1/7P/4K3 w - - 4 38")
    best_move = move.minimax_root(2, b)
    assert "e5h5" == best_move.uci()


def test_minimax():
    b = chess.Board("4kr2/4b3/8/2p1R2p/4n1p1/3q2P1/7P/4K3 w - - 4 38")
    best_value = move.minimax(1, b, True)
    assert -13 == best_value

    best_value = move.minimax(3, b, True)
    assert -18 == best_value
