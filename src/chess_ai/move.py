import time
from typing import List

from tqdm import tqdm

import chess_ai.chess_engine as chess
from chess_ai.evaluate import evaluate_board
from chess_ai.log import debug_info


def next_move(depth: int, board: chess.GameState, debug=True) -> chess.Move:
    if debug:
        debug_info["nodes_searched"] = 0

    move = minimax_root(depth, board)
    return move


def get_ordered_moves(board: chess.GameState) -> List[chess.Move]:
    def orderer(move):
        return evaluate_board(board, move)

    in_order = sorted(
        board.getValidMoves(), key=orderer, reverse=(board.white_to_move)
    )
    return list(in_order)


def minimax_root(depth: int, board: chess.GameState) -> chess.Move:
    maximize = board.white_to_move
    best_move = -float("inf") if maximize else float("inf")

    moves = get_ordered_moves(board)

    if len(moves) == 0:
        raise Exception("Game is Over!")

    best_move_found = moves[0]

    start_time = time.time()
    allocated_time = 1.0

    for move in tqdm(moves, desc="Searching moves..."):
        if time.time() - start_time >= allocated_time:
            return best_move_found

        board.makeMove(move)
        value = minimax(depth - 1, board, not maximize)

        board.undoMove()
        if maximize and value >= best_move:
            best_move = value
            best_move_found = move
        elif not maximize and value <= best_move:
            best_move = value
            best_move_found = move

    return best_move_found


def minimax(
    depth: int,
    board: chess.GameState,
    is_maximising_player: bool,
) -> float:
    debug_info["nodes_searched"] += 1

    if depth == 0:
        return evaluate_board(board)

    best_move = -float("inf") if is_maximising_player else float("inf")
    moves = get_ordered_moves(board)

    if is_maximising_player:
        for move in moves:
            board.makeMove(move)
            curr_move = minimax(depth - 1, board, not is_maximising_player)
            if curr_move > best_move:
                best_move = curr_move
                debug_info["move_details"][depth] = move
            board.undoMove()
    else:
        for move in moves:
            board.makeMove(move)
            curr_move = minimax(depth - 1, board, not is_maximising_player)
            if curr_move < best_move:
                best_move = curr_move
                debug_info["move_details"][depth] = move
            board.undoMove()
    return best_move
