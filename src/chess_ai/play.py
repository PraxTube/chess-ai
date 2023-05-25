import chess_ai.chess_engine as chess
from chess_ai.move import next_move
from chess_ai import inout
from chess_ai import log


def main_loop(depth, debug_info, turn_limit=-1):
    board = chess.Board()

    while turn_limit != 0:
        turn_limit -= 1

        best_move = next_move(depth, board, debug_info)
        if not best_move:
            game_over(board)
            break
        inout.print_board(board, best_move, debug_info)

        board.make_move(best_move)
        log.append_log_file(best_move, debug_info)
        log.append_extensive_log_file(board, debug_info)


def game_over(board):
    if not board.checkmate:
        raise ValueError("The board indicated that it's not checkmate!", board.fen())

    moves = board.legal_moves()
    if moves:
        raise ValueError(
            "Checkmate! But board indicates that there are possible moves!", moves
        )

    winner = "White - Max" if not board.white_to_move else "Black - Min"
    print(f"\n\nCHECKMATE!\n---\nThe winner is {winner}!")
    print("The end baord is:\n")
    print(board)
    print(f"\nFEN:\n{board.fen()}")
