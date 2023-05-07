import os
from io import StringIO
import timeit
import contextlib

import chess

from chess_ai import move
from chess_ai import evaluate


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


def bench_move(board, move):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            board.push(move)
            board.pop()


def bench_best_move(depth, board):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            move.next_move(depth, board)


def bench_evaluate(board, move=None):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            evaluate.evaluate_board(board, move)


def benchmark_template(msg, n, result_func, use_seconds):
    print(f"\n==========\n{msg}\n==========\n")
    boards = get_boards()

    for board in boards:
        result = result_func.__call__(board)

        if use_seconds:
            total_time = round(result, 4)
            average_time = round(result / n * 1000, 2)
        else:
            total_time = round(result * 1000, 4)
            average_time = round(result / n * 1000 * 1000, 2)

        print(
            "Total: {}ms, Average: {}µs - {} - {}".format(
                total_time,
                average_time,
                board.legal_moves.count(),
                board.fen().split()[0],
            )
        )


def benchmark_legal_moves():
    n = 10000

    def bench(board):
        return timeit.timeit(
            lambda: bench_legal_moves(board),
            number=n,
            globals=locals(),
        )

    benchmark_template("Benchmark legal moves generation", n, bench, False)


def benchmark_move():
    n = 10000

    def bench(board):
        move = list(board.legal_moves)[0]
        return timeit.timeit(
            lambda: bench_move(board, move),
            number=n,
            globals=locals(),
        )

    benchmark_template("Benchmark making moves", n, bench, False)


def benchmark_evaluate():
    n = 1000

    def bench_without_move(board):
        return timeit.timeit(
            lambda: bench_evaluate(board),
            number=n,
            globals=locals(),
        )

    def bench_with_move(board):
        move = list(board.legal_moves)[0]
        return timeit.timeit(
            lambda: bench_evaluate(board, move),
            number=n,
            globals=locals(),
        )

    benchmark_template(
        "Benchmark evaluate board WITHOUT move", n, bench_without_move, False
    )
    benchmark_template("Benchmark evaluate board WITH move", n, bench_with_move, False)


def benchmark_best_move():
    n = 100

    def bench(board):
        return timeit.timeit(
            lambda: bench_best_move(1, board),
            number=n,
            globals=locals(),
        )

    benchmark_template("Benchmark best move generation", n, bench, True)


def benchmark():
    benchmark_legal_moves()
    benchmark_move()
    benchmark_evaluate()
    benchmark_best_move()


if __name__ == "__main__":
    benchmark()
