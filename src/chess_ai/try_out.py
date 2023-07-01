import random
import chess
import  chess_engine as engine
import time
import evaluate as eval

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

evaluate_runtimes = []


evaluate_scores = []


for x in fen_strings:

    board = engine.Board(fen_board= x)

    start_time = time.time()

    score = eval.evaluate_board(board)

    end_time = time.time()

    evaluate_runtimes.append(end_time)
    evaluate_scores.append(score)



print("The average Runtime of the piece function is: " + str(sum(evaluate_runtimes) / len(evaluate_runtimes)))

print("The average score of the piece  function is: " + str(sum(evaluate_scores) / len(evaluate_scores)))

print(evaluate_scores)