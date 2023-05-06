import os
from io import StringIO
import timeit
import contextlib

import chess

from chess_ai import move


script_dir = os.path.dirname(os.path.abspath(__file__))
benchmark_file = os.path.join(script_dir, "boards_and_moves.txt")


def suppress_prints():
    return StringIO()


def get_boards():
    with open(benchmark_file, "r") as f:
        content = f.readlines()
        boards = [chess.Board(x.split(";")[0]) for x in content]
        return boards


def get_legal_moves():
    with open(benchmark_file, "r") as f:
        content = f.readlines()
        legal_moves = [x.split(",")[1] for x in content]
        return legal_moves


def bench_legal_moves(board):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            board.legal_moves


def bench_best_move(depth, board):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            move.next_move(depth, board)


def benchmark_legal_moves():
    print("\n==========\nBenchmark legal moves generation\n==========\n")
    boards = get_boards()

    for board in boards:
        number_of_runs = 10000
        result = timeit.timeit(
            lambda: bench_legal_moves(board),
            number=number_of_runs,
            globals=locals(),
        )
        print(
            "Total: {}ms, Average: {}µs - {} - {}".format(
                round(result * 1000, 4),
                round(result / number_of_runs * 1000 * 1000, 2),
                board.legal_moves.count(),
                board.fen().split()[0],
            )
        )


def benchmark_best_move():
    print("\n==========\nBenchmark best move generation\n==========\n")
    boards = get_boards()

    for board in boards:
        number_of_runs = 100
        result = timeit.timeit(
            lambda: bench_best_move(1, board),
            number=number_of_runs,
            globals=locals(),
        )
        print(
            "Total: {}s, Average: {}ms - {} - {}".format(
                round(result, 4),
                round(result / number_of_runs * 1000, 2),
                board.legal_moves.count(),
                board.fen().split()[0],
            )
        )


def benchmark():
    benchmark_legal_moves()
    benchmark_best_move()


if __name__ == "__main__":
    benchmark()
