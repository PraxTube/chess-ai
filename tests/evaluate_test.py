import chess_ai.chess_engine as chess

from chess_ai.evaluate import evaluate_board


def test_evaluate_board():
    """
    This test is not to check that the output works,
    but rather to test if the function changes the given
    board in a way we don't want it to.
    """
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
