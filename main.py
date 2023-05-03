import random
import time
from typing import Dict, List, Any

import numpy as np
import chess


board = chess.Board()
debug_info = {"nodes_searched": 0}


def pull_random_move():
    random_index = random.randint(0, board.legal_moves.count() - 1)
    moves = [x for x in board.legal_moves]
    move = str(moves[random_index])
    board.push_san(move)


def evaluate_board(board, move):
    board.push(move)
    fen_string = board.fen().split()[0]
    board.pop()

    piece_chars = ["p", "b", "n", "r", "q", "k"]
    white_pieces = np.array([fen_string.count(x.upper()) for x in piece_chars])
    black_pieces = np.array([fen_string.count(x) for x in piece_chars])

    multiplication_mask = np.array([1, 3, 3, 5, 9, 900])
    return white_pieces.dot(multiplication_mask) - black_pieces.dot(multiplication_mask)


def copy_mv(board, san_move):
    new_board = board.copy()
    new_board.push_san(san_move)
    return new_board


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
    """
    Get legal moves.
    Attempt to sort moves by best to worst.
    Use piece values (and positional gains/losses) to weight captures.
    """
    end_game = check_end_game(board)

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
        value = minimax(depth - 1, board, -float("inf"), float("inf"), not maximize)
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


def minimax(board, depth, maximizing_player):
    global boards_searched
    boards_searched += 1

    if depth == 0 or board.legal_moves.count() == 0:
        return evaluate_board(board)

    if maximizing_player:
        value = -100000
        for move in board.legal_moves:
            value = max(value, minimax(copy_mv(board, str(move)), depth - 1, False))
        return value
    else:
        value = 100000
        for move in board.legal_moves:
            value = min(value, minimax(copy_mv(board, str(move)), depth - 1, True))
        return value


def minimax(
    depth: int,
    board: chess.Board,
    is_maximising_player: bool,
) -> float:
    debug_info["nodes_searched"] += 1

    if board.is_checkmate():
        return 0
    elif board.is_game_over():
        return 0

    if depth == 0:
        return evaluate_board(board)

    best_move = -float("inf") if maximizing_player else float("inf")
    moves = get_ordered_moves(board)

    if is_maximising_player:
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1, board, alpha, beta, not is_maximising_player)
            best_move = max(best_move, curr_move)
            board.pop()

            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move
    else:
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1, board, alpha, beta, not is_maximising_player)
            best_move = min(best_move, curr_move)
            board.pop()

            beta = min(beta, best_move)
            if beta <= alpha:
                return best_move
    return best_move


def get_move_from_value(board, best_value):
    for move in board.legal_moves:
        if best_value == evaluate_board(copy_mv(board, str(move))):
            return str(move)
    raise ValueError("There aren't any legal moves that match the best value!")


def print_board(best_move):
    evaluation_ratio = evaluate_board(board)
    print("\n------------\n")
    print(board)
    print(f"\nCurrent Evaluation of the board is: {evaluation_ratio}")
    print(f"Best move has evaluation of {best_move}")
    print(f"Number of boards searched: {boards_searched}")


def main():
    white_turn = True
    while True:
        global boards_searched
        boards_searched = 0

        best_move = minimax(board, 3, white_turn)

        if not best_move:
            print("\n\n\n-------\nGame Over\n\n----")
        print_board(best_move)

        board.push_san(get_move_from_value(board, best_move))

        white_turn = not white_turn


def test():
    print(board)

    print("\n\n\n\n\n")

    print(copy_mv(board, "e4"))

    print("\n\n\n\n\n")

    print(board)


if __name__ == "__main__":
    main()
