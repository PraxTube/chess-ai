import chess_ai.chess_engine as chess
from chess_ai.move import next_move
from chess_ai import inout
from chess_ai import log


def main_loop(depth, do_debug=True):
    if do_debug:
        main_loop_debug
    else:
        main_loop_no_debug


def main_loop_debug(depth):
    board = chess.GameState()

    for i in range(1, depth):
        log.debug_info["move_details"][i] = None

    while True:
        best_move = next_move(depth, board)
        if not best_move:
            print("\n\n\n-------\nGame Over\n\n----")
            break
        inout.print_board(board, best_move)

        board.makeMove(best_move)
        log.append_log_file(best_move)
        log.append_extensive_log_file(board)


def main_loop_no_debug(depth):
    board = chess.GameState()

    while True:
        best_move = next_move(depth, board)
        if not best_move:
            break

        board.makeMove(best_move)
