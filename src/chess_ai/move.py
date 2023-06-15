import time
import random
from typing import List

from tqdm import tqdm

import chess_ai.chess_engine as chess
from chess_ai.evaluate import evaluate_board
from chess_ai.evaluate import INF


def next_move(depth: int, board: chess.Board, debug_info) -> chess.Move:
    debug_info.reset_nodes()

    move = alpha_beta_root(depth, board, debug_info)
    return move


def get_ordered_moves(board: chess.Board) -> List[chess.Move]:
    def orderer(move):
        return evaluate_board(board, move, board.white_to_move)

    ordered_moves = list(
        sorted(board.legal_moves(), key=orderer, reverse=(board.white_to_move))
    )
    return ordered_moves


def alpha_beta_root(depth: int, board: chess.Board, debug_info) -> chess.Move:
    best_move = -INF if board.white_to_move else INF

    moves = get_ordered_moves(board)
    if len(moves) == 0:
        return None

    best_move_found = moves[0]

    start_time = time.time()
    allocated_time = 100
    # für jeden einezelnen move der möglichen
    for move in tqdm(moves, desc="Searching moves..."):
        if not board.white_to_move:
            index = random.randint(0, len(moves) - 1)
            return moves[index]

        if time.time() - start_time >= allocated_time:
            return best_move_found

        board.make_move(move)
        value = alpha_beta(depth - 1, board, debug_info)
        board.undo_move()

        if board.white_to_move and value >= best_move:
            best_move = value
            best_move_found = move
        elif not board.white_to_move and value <= best_move:
            best_move = value
            best_move_found = move
    return best_move_found


def alpha_beta(depth: int, board: chess.Board, debug_info) -> int:
    if board.checkmate or board.stalemate:
        return evaluate_board(board) + depth

    if board.white_to_move:
        return alpha_beta_max(-INF, INF, depth, board, debug_info)
    else:
        return alpha_beta_min(-INF, INF, depth, board, debug_info)


def alpha_beta_max(alpha, beta, depth, board, debug_info):
    debug_info.increment_nodes()

    if depth == 0:
        return evaluate_board(board)

    moves = get_ordered_moves(board)
   # 
    for move in moves:
        board.make_move(move)
        current_value = alpha_beta_min(alpha, beta, depth - 1, board, debug_info)
        board.undo_move()

        if current_value >= beta:
            return beta
        if current_value > alpha:
            alpha = current_value
            debug_info.move_details[depth] = move.coordinate()
    return alpha


def alpha_beta_min(alpha, beta, depth, board, debug_info):
    debug_info.increment_nodes()

    if depth == 0:
        return evaluate_board(board)

    moves = get_ordered_moves(board)

    for move in moves:
        board.make_move(move)
        current_value = alpha_beta_max(alpha, beta, depth - 1, board, debug_info)
        board.undo_move()

        if current_value <= alpha:
            return alpha
        if current_value < beta:
            beta = current_value
            debug_info.move_details[depth] = move.coordinate()
    return beta
