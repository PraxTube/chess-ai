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

# für eine zustand des spielbretts wir deine liste von möglichen spielzügen zurückgegeben
# und es kommt darauf an welche farbe am ug ist in welcher reihenfolge die liste zurückgegeben wird
def get_ordered_moves(board: chess.GameState) -> List[chess.Move]:
    def orderer(move):
        return evaluate_board(board, move, board.white_to_move)

    in_order = sorted(board.getValidMoves(), key=orderer, reverse=(board.white_to_move))
    return list(in_order)


def minimax_root(depth: int, board: chess.GameState) -> chess.Move:
    # flah ob weiß oder schwarz am zug ist
    maximize = board.white_to_move
    #best move wird hier erstmal auf eine sehr große zahl gesetzt, kommt drauf an wer am zug ist ist sie positiv oder negativ
    best_move = -float("inf") if maximize else float("inf")

    moves = get_ordered_moves(board)

    if len(moves) == 0:
        raise Exception("Game is Over!")

    best_move_found = moves[0]

    start_time = time.time()
    allocated_time = 100
    # für jeden einezelnen move der möglichen
    for move in tqdm(moves, desc="Searching moves..."):
        # wenn keine zeit mehr ist wird der zug zurückgegeben
        if time.time() - start_time >= allocated_time:
            return best_move_found

        board.makeMove(move)
        value = alpha_beta(depth - 1, board, not maximize)
        board.undoMove()

        if maximize and value >= best_move:
            best_move = value
            best_move_found = move
        elif not maximize and value <= best_move:
            best_move = value
            best_move_found = move
    return best_move_found


def alpha_beta(
    depth: int,
    board: chess.GameState,
    is_maximising_player: bool,
) -> float:
    if is_maximising_player:
        # hier werden wieder sehr große werte für alpha und beta riengegeben
        return alpha_beta_max(-float("inf"), float("inf"), depth, board)
    else:
        return alpha_beta_min(-float("inf"), float("inf"), depth, board)

# für weiß
def alpha_beta_max(alpha, beta, depth, board):
    debug_info["nodes_searched"] += 1

    if depth == 0:
        return evaluate_board(board)

    moves = get_ordered_moves(board)
   # 
    for move in moves:
        board.makeMove(move)
        current_value = alpha_beta_min(alpha, beta, depth - 1, board)
        board.undoMove()

        if current_value >= beta:
            return beta
        if current_value > alpha:
            alpha = current_value
            debug_info["move_details"][depth] = move
    return alpha


def alpha_beta_min(alpha, beta, depth, board):
    debug_info["nodes_searched"] += 1

    if depth == 0:
        return evaluate_board(board)

    moves = get_ordered_moves(board)

    for move in moves:
        board.makeMove(move)
        current_value = alpha_beta_max(alpha, beta, depth - 1, board)
        board.undoMove()

        if current_value <= alpha:
            return alpha
        if current_value < beta:
            beta = current_value
            debug_info["move_details"][depth] = move
    return beta
