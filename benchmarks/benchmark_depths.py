import os
from io import StringIO
import timeit
import contextlib

import chess_ai.chess_engine as chess
from chess_ai import move


script_dir = os.path.dirname(os.path.abspath(__file__))
benchmark_file = os.path.join(script_dir, "boards_and_moves.txt")
current_best_move = None
current_debug_info = {}


def suppress_prints():
    return StringIO()


def bench_best_move(depth, board):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            global current_best_move
            global current_debug_info

            best_move, debug_info = move.next_move(depth, board, return_debug_info=True)
            current_best_move = best_move
            current_debug_info = debug_info


def benchmark_template(msg, n, result_func, depth, board):
    print(f"\n=========\n{msg}\n=========\n")

    result = result_func.__call__(depth, board)

    msg = "Total: {}s, Average: {}ms - {} - {}"
    total_time = round(result, 4)
    average_time = round(result / n * 1000, 2)

    print(
        msg.format(
            total_time,
            average_time,
            len(board.getValidMoves()),
            board.fen(),
        )
    )

    move_details = [str(x) for x in current_debug_info["move_details"].values()]
    move_details.reverse()

    return str(current_best_move), (
        current_debug_info["nodes_searched"],
        move_details,
    )


def benchmark_best_move(depth, boards, n, msg):
    def bench(depth, board):
        return timeit.timeit(
            lambda: bench_best_move(depth, board),
            number=n,
            globals=locals(),
        )

    return [benchmark_template(msg, n, bench, depth, board) for board in boards]


def benchmark():
    max_depth = 5
    number_of_runs = [500, 50, 20, 5, 1]
    boards = [
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "r1bqkbnr/pppppppp/n7/6N1/8/8/PPPPPPPP/RNBQKB1R b - - 0 1",
    ]
    msg = "Benchmark best move for depth #, number of iterations $"

    for i in range(max_depth):
        info = benchmark_best_move(
            i + 1,
            [chess.GameState(board) for board in boards],
            number_of_runs[i],
            msg.replace("#", str(i + 1)).replace("$", str(number_of_runs[i])),
        )
        print(info)


if __name__ == "__main__":
    benchmark()
