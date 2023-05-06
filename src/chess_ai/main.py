import chess

from chess_ai.move import next_move
from chess_ai import inout
from chess_ai import log


def main():
    depth = 3
    board = chess.Board()

    for i in range(1, depth):
        log.debug_info["move_details"][i] = None

    while True:
        best_move = next_move(depth, board)
        if not best_move:
            print("\n\n\n-------\nGame Over\n\n----")
            break
        inout.print_board(board, best_move)

        board.push(best_move)
        log.append_log_file(best_move)
        log.append_extensive_log_file(board)


if __name__ == "__main__":
    main()
