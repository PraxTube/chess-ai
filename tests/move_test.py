import chess_ai.chess_engine as chess
from chess_ai import move
from chess_ai.log import DebugInfo


def test_next_move():
    depth = 1
    debug_info = DebugInfo(depth)

    b = chess.Board()
    legal_moves = b.legal_moves()

    best_move = move.next_move(depth, b, debug_info)
    assert best_move in legal_moves
