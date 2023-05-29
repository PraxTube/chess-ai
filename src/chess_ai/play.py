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
            game_over(board)
            break

        best_move = next_move(depth, board, debug_info)
        if not best_move:
            game_over(board)
            break

        board.make_move(best_move)
        inout.print_board(board, best_move, debug_info)

        log.append_log_file(best_move, debug_info)
        log.append_extensive_log_file(board, debug_info)

    if board.checkmate:
        return 1 if not board.white_to_move else 2
    elif board.stalemate:
        return 0

    if turn_limit == 0:
        return -1
    raise ValueError("The board didn't end yet!", board.fen())


def game_over(board):
    if not (board.checkmate or board.stalemate):
        raise ValueError("The board indicated that it's not over yet!", board.fen())

    moves = board.legal_moves()
    if len(moves) != 0:
        board.check_king_of_the_hill_condition()
        if not board.checkmate:
            raise ValueError(
                "The board indicates a King of the Hill win, but it's not!", board.fen()
            )

    winner = "White - Max" if not board.white_to_move else "Black - Min"
    print(f"\n\nCHECKMATE!\n---\nThe winner is {winner}!")
    print("The end board is:\n")
    print(board)
    print(f"\nFEN:\n{board.fen()}")
