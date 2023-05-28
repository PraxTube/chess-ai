import os

import chess_ai.chess_engine as chess
from chess_ai.evaluate import evaluate_board
from chess_ai.evaluate import INF


def test_board_change():
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"
    board = chess.Board(start_fen)

    _ = evaluate_board(board)
    assert start_fen == board.fen()

    current_fen = start_fen
    depth = 10
    for i in range(depth):
        for move in board.legal_moves():
            _ = evaluate_board(board, move)
            assert current_fen == board.fen()

        board.make_move(move)
        current_fen = board.fen()

    for i in range(depth):
        board.undo_move()
    assert start_fen == board.fen()

    current_fen = start_fen
    depth = 150
    for i in range(depth):
        for move in board.legal_moves():
            _ = evaluate_board(board, move)
            assert current_fen == board.fen()

        board.make_move(move)
        current_fen = board.fen()

    for i in range(depth):
        board.undo_move()
    assert start_fen == board.fen()


def test_evaluation():
    error_range = 50
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "boards_and_evaluations.csv"), "r") as f:
        data = f.readlines()

    for data_row in data:
        data_row = data_row.rstrip()
        fen, expected_value = data_row.split(",")
        if expected_value == "INF":
            expected_value = INF
        elif expected_value == "-INF":
            expected_value = -INF
        else:
            expected_value = int(expected_value)

        board = chess.Board(fen)
        actual_value = evaluate_board(board)

        err_msg = """
Expected value: {}
Actual Value: {}
Error Range: {}
Fen string: {}
        """.format(
            expected_value, actual_value, error_range, fen
        )

        assert abs(expected_value - actual_value) <= error_range, err_msg


def test_castling_evaluation():
    pre_castling_board = chess.Board(
        "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 1 5"
    )
    post_castling_board = chess.Board(
        "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 b kq - 2 5"
    )

    assert evaluate_board(pre_castling_board) < evaluate_board(post_castling_board)


def test_checkmate_evaluation():
    checkmate_board = chess.Board(
        "r1bqk1nr/pppp1Qpp/2n5/2b1p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"
    )
    assert checkmate_board.checkmate
    assert INF == evaluate_board(checkmate_board)

    checkmate_board = chess.Board("1k6/1Q6/1K6/2p5/1pPp4/1P1P4/8/8 b - - 15 8")
    assert checkmate_board.checkmate
    assert INF == evaluate_board(checkmate_board)

    checkmate_board = chess.Board(
        "rnb1k1nr/pppp1ppp/8/2b1p3/2B1P3/2N5/PPPP1qPP/R1BQK1NR w KQkq - 0 1"
    )
    assert checkmate_board.checkmate
    assert -INF == evaluate_board(checkmate_board)


def test_stalemate_evaluation():
    stalemate_board = chess.Board("1k6/1P6/1K6/8/8/8/8/8 b - - 0 1")
    assert stalemate_board.stalemate
    assert -50 > evaluate_board(stalemate_board)

    stalemate_board = chess.Board("8/8/8/5k2/5p2/5K2/r7/8 w - - 0 1")
    assert stalemate_board.stalemate
    assert 50 < evaluate_board(stalemate_board)


def test_king_of_the_hill_evaluation():
    checkmate_board = chess.Board("5r2/8/2p3p1/3kp2p/8/P2P4/1PP5/2KR4 w - - 0 1")
    assert checkmate_board.checkmate
    assert -INF == evaluate_board(checkmate_board)

    checkmate_board = chess.Board("8/8/8/4k3/5p2/5K2/r7/8 w - - 0 1")
    assert checkmate_board.checkmate
    assert -INF == evaluate_board(checkmate_board)

    checkmate_board = chess.Board("3r4/2k5/2p5/8/4K3/8/8/8 b - - 0 1")
    assert checkmate_board.checkmate
    assert INF == evaluate_board(checkmate_board)
