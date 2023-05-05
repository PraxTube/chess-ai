import random
import time
from datetime import datetime
from typing import Dict, List, Any

import numpy as np
import chess


board = chess.Board()
debug_info = {"nodes_searched": 0, "move_details": {}}


def evaluate_board(board, move=None):
    if move:
        board.push(move)
        fen_string = board.fen().split()[0]
        board.pop()
    else:
        fen_string = board.fen().split()[0]

    piece_chars = ["p", "b", "n", "r", "q", "k"]
    white_pieces = np.array([fen_string.count(x.upper()) for x in piece_chars])
    black_pieces = np.array([fen_string.count(x) for x in piece_chars])

    multiplication_mask = np.array([1, 3, 3, 5, 9, 900])
    return white_pieces.dot(multiplication_mask) - black_pieces.dot(multiplication_mask)


def next_move(depth: int, board: chess.Board, debug=True) -> chess.Move:
    debug_info.clear()
    debug_info["nodes"] = 0
    t_0 = time.time()

    move = minimax_root(depth, board)

    debug_info["time"] = time.time() - t_0
    if debug == True:
        print(f"\n------\nDebug Info:\n{debug_info}")
    return move


def get_ordered_moves(board: chess.Board) -> List[chess.Move]:
    def orderer(move):
        return evaluate_board(board, move)

    in_order = sorted(
        board.legal_moves, key=orderer, reverse=(board.turn == chess.WHITE)
    )
    return list(in_order)


def minimax_root(depth: int, board: chess.Board) -> chess.Move:
    maximize = board.turn == chess.WHITE
    best_move = -float("inf") if maximize else float("inf")

    moves = get_ordered_moves(board)

    if len(moves) == 0:
        raise Exception("Game is Over!")

    best_move_found = moves[0]

    for move in moves:
        board.push(move)
        value = minimax(depth - 1, board, not maximize)
        if board.can_claim_draw():
            value = 0.0

        board.pop()
        if maximize and value >= best_move:
            best_move = value
            best_move_found = move
        elif not maximize and value <= best_move:
            best_move = value
            best_move_found = move

    return best_move_found


def minimax(
    depth: int,
    board: chess.Board,
    is_maximising_player: bool,
) -> float:
    debug_info["nodes_searched"] += 1

    if board.is_checkmate():
        pass
    elif board.is_game_over():
        pass

    if depth == 0:
        return evaluate_board(board)

    best_move = -float("inf") if is_maximising_player else float("inf")
    moves = get_ordered_moves(board)

    if is_maximising_player:
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1, board, not is_maximising_player)
            if curr_move > best_move:
                best_move = curr_move
                debug_info["move_details"][depth] = move
            board.pop()
    else:
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1, board, not is_maximising_player)
            if curr_move < best_move:
                best_move = curr_move
                debug_info["move_details"][depth] = move
            board.pop()
    return best_move


def print_board(best_move):
    evaluation_ratio = evaluate_board(board)
    boards_searched = debug_info["nodes_searched"]
    move_details = debug_info["move_details"]
    print("\n------------\n")
    print(board)
    print(f"\nCurrent Evaluation of the board is: {evaluation_ratio}")
    print(f"Best move has evaluation of {best_move}")
    print(f"Number of boards searched: {boards_searched}")
    print(f"Move Details:\n{move_details}")


def get_log_name():
    date_str = datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
    log_file = f"log-{date_str}.txt"
    return log_file


def get_extensive_log_name():
    date_str = datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
    log_file = f"log-details-{date_str}.txt"
    return log_file


def append_log_file(file_name, last_move):
    with open(f"logs/{file_name}", "a") as f:
        move_str = f"{last_move.uci()}\n"
        f.writelines(move_str)


def append_extensive_log_file(file_name):
    with open(f"logs/{file_name}", "a") as f:
        reversed_moves = [x.uci() for x in debug_info["move_details"].values()]
        reversed_moves.reverse()
        moves = " ".join(reversed_moves)
        content = f"{board.fen()},{moves}\n"
        f.writelines(content)


def main():
    depth = 3

    log_file = get_log_name()
    extensive_log_file = get_extensive_log_name()
    for i in range(1, depth):
        debug_info["move_details"][i] = None

    while True:
        debug_info["nodes_searched"] = 0

        best_move = minimax_root(depth, board)
        if not best_move:
            print("\n\n\n-------\nGame Over\n\n----")
        print_board(best_move)

        board.push(best_move)
        append_log_file(log_file, best_move)
        append_extensive_log_file(extensive_log_file)


def test():
    print(board)

    print("\n\n\n\n\n")

    print(copy_mv(board, "e4"))

    print("\n\n\n\n\n")

    print(board)


if __name__ == "__main__":
    main()
