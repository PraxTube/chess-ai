import chess_ai.chess_engine as chess
from chess_ai.move import next_move
from chess_ai import inout
from chess_ai import log


def main_loop(depth, do_debug=True):
    if do_debug:
        main_loop_debug(depth)
    else:
        main_loop_no_debug(depth)


def main_loop_debug(depth):
    board = chess.GameState()

    for i in range(1, depth):
        log.debug_info["move_details"][i] = None

    while True:
        best_move = next_move(depth, board)
        if not best_move:
            game_over(board)
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


def game_over(board):
    if not board.checkmate:
        raise ValueError("The board indicated that it's not checkmate!", board.fen())

    moves = board.getValidMoves()
    if moves:
        raise ValueError(
            "Checkmate! But board indicates that there are possible moves!", moves
        )

    winner = "White - Max" if not board.white_to_move else "Black - Min"
    print(f"\n\nCHECKMATE!\n---\nThe winner is {winner}!")
    print("The end baord is:\n")
    print(board)
    print(f"\nFEN:\n{board.fen()}")
