import random
import chess
import  chess_engine as engine
import time
import test2 as eval

fen_strings = []

for _ in range(100):
    board = chess.Board()
    random_moves = random.randint(10, 30)  # Generate a random number of moves
    
    for _ in range(random_moves):
        legal_moves = list(board.legal_moves)
        random_move = random.choice(legal_moves)
        board.push(random_move)
    
    fen_string = board.fen()
    fen_strings.append(fen_string)

# ------------- Board evaluation performance test ----------------

test2_runtimes = []
evaluate_runtimes = []

test2_scores = []
evaluate_scores = []


for x in fen_strings:

    board = engine.Board(fen_board= x)

    start_time = time.time()

    score = eval.evaluate_board(board, board.white_to_move)

    end_time = time.time()

    test2_runtimes.append(end_time)
    test2_scores.append(score)

print("The average Runtime of the function is: " + sum(test2_runtimes) / len(test2_runtimes))