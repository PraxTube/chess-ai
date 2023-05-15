import os

import chess_ai.chess_engine as chess


def test_fen():
    board = chess.GameState()
    assert "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1" == board.fen()

    board = chess.GameState(
        "r3k2r/ppp1bppp/b1n2n2/1N2B3/2B1q3/2Q1PN2/PPP2PPP/R3K2R b - - 0 1"
    )
    assert (
        "r3k2r/ppp1bppp/b1n2n2/1N2B3/2B1q3/2Q1PN2/PPP2PPP/R3K2R b - - 0 1"
        == board.fen()
    )


def test_setup_fen_board():
    board = chess.GameState(
        "R2Q1RK1/P2B1PPP/1PNP1N2/2P1P3/2pp4/2pbp2p/p2n1pp1/1rbq1rk1 w - - 0 1"
    )
    assert (
        "R2Q1RK1/P2B1PPP/1PNP1N2/2P1P3/2pp4/2pbp2p/p2n1pp1/1rbq1rk1 w - - 0 1"
        == board.fen()
    )


def test_make_move():
    board = chess.GameState()
    move = chess.Move((6, 4), (4, 4), board.board)
    board.makeMove(move)

    assert "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b - - 0 1" == board.fen()


def test_undo_move():
    board = chess.GameState()
    move = chess.Move((6, 4), (4, 4), board.board)
    board.makeMove(move)

    assert "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b - - 0 1" == board.fen()

    board.undoMove()

    assert "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1" == board.fen()


def test_get_valid_moves():
    board = chess.GameState()
    legal_moves = board.getValidMoves()

    assert 20 == len(legal_moves)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    boards_and_moves_file = os.path.join(script_dir, "boards_and_moves.txt")

    with open(boards_and_moves_file, "r") as f:
        boards_and_moves = [
            (
                x.rstrip().split(";")[0],
                [y for y in x.rstrip().split(";")[1].replace(" ", "").split(",")],
            )
            for x in f.readlines()
        ]

    for board, expected_moves in boards_and_moves:
        board = chess.GameState(board)
        actual_moves = [str(x) for x in board.getValidMoves()]

        expected_moves.sort()
        actual_moves.sort()

        assert len(expected_moves) == len(actual_moves)
        assert expected_moves == actual_moves


def test_get_all_possible_moves():
    board = chess.GameState()
    possible_moves = board.getAllPossibleMoves()

    assert 20 == len(possible_moves)
