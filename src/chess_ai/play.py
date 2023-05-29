import chess_ai.chess_engine as chess
from chess_ai.move import next_move
from chess_ai import inout
from chess_ai import log


def main_loop(depth, debug_info, turn_limit=-1, fen=""):
    if fen == "":
        board = chess.Board()
    else:
        board = chess.Board(fen)

    while turn_limit != 0:
        turn_limit -= 1

        if board.checkmate:
            break

        best_move = next_move(depth, board, debug_info)
        if not best_move:
            break
        board.make_move(best_move)

        inout.print_board(board, best_move, debug_info)
        log.append_log_file(best_move, debug_info)
        log.append_extensive_log_file(board, debug_info)

    if board.checkmate:
        return 1 if not board.white_to_move else 2, board
    elif board.stalemate:
        return 0, board

    if turn_limit == 0:
        return -1, board
    raise ValueError("The board didn't end yet!", board.fen())
