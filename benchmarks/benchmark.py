import os
from io import StringIO
import timeit
import contextlib

import pandas as pd

from chess_ai import chess_engine as chess
from chess_ai import move
from chess_ai import evaluate
from chess_ai.log import DebugInfo


script_dir = os.path.dirname(os.path.abspath(__file__))
benchmark_file = os.path.join(script_dir, "boards_and_moves.txt")
benchmark_dataframe = pd.DataFrame(
    columns=["Category", "Total", "Average", "Valid Moves", "Fen"]
)
stage = ["Early", "Mid", "Late"]

msgs = [
    "Fen Conversion",
    "Legal Move Gen",
    "Making Move",
    "Evaluate Board WITHOUT Move",
    "Evaluate Board",
    "Best Move Gen",
]


def benchmark_to_dataframe(msg_index, total_time, average_time, valid_moves, fen):
    if msg_index == 3:
        return

    if not 0 <= msg_index < len(msgs):
        raise ValueError("The given index is outside of it's bounds!", msgs, msg_index)

    row_data = {
        "Category": msgs[msg_index],
        "Total": round(total_time, 2),
        "Average": round(average_time, 2),
        "Valid Moves": valid_moves,
        "Fen": fen,
    }
    benchmark_dataframe.loc[len(benchmark_dataframe)] = row_data


def suppress_prints():
    return StringIO()


def get_boards(file):
    with open(os.path.join(script_dir, file), "r") as f:
        content = f.readlines()
        boards = [chess.Board(x) for x in content]
        return boards


def get_boards_list():
    files = ["early_game_boards.txt", "mid_game_boards.txt", "late_game_boards.txt"]
    boards_list = []
    for file in files:
        boards_list.append(get_boards(file))
    return boards_list


def bench_to_fen(board):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            board.fen()


def bench_legal_moves(board):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            board.legal_moves()


def bench_move(board, move):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            board.make_move(move)
            board.undo_move()


def bench_evaluate(board, move=None):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            evaluate.evaluate_board(board, move, use_table=False)


def bench_best_move(depth, board, debug_info):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            move.next_move(depth, board, debug_info)


def seconds_format(result, n):
    msg = "Total: {}s, Average: {}ms - {} - {}"
    total_time = round(result, 4)
    average_time = round(result / n * 1000, 2)
    return msg, total_time, average_time


def milliseconds_format(result, n):
    msg = "Total: {}ms, Average: {}µs - {} - {}"
    total_time = round(result * 1000, 4)
    average_time = round(result / n * 1000 * 1000, 2)
    return msg, total_time, average_time


def benchmark_template(msg_index, n, result_func, boards, use_seconds):
    print(f"\n==========\n{msgs[msg_index]}\n==========\n")
    for i, board in enumerate(boards):
        result = result_func.__call__(board)
        number_of_valid_moves = len(board.legal_moves())

        if use_seconds:
            msg, total_time, average_time = seconds_format(result, n)
        else:
            msg, total_time, average_time = milliseconds_format(result, n)

        print(
            msg.format(
                total_time,
                average_time,
                number_of_valid_moves,
                board.fen(),
            )
        )

        if i == 0:
            benchmark_to_dataframe(
                msg_index,
                total_time,
                average_time,
                number_of_valid_moves,
                board.fen(),
            )


def benchmark_to_fen(boards):
    n = 10000

    def bench(board):
        return timeit.timeit(
            lambda: bench_to_fen(board),
            number=n,
            globals=locals(),
        )

    benchmark_template(0, n, bench, boards, False)


def benchmark_legal_moves(boards):
    n = 1000

    def bench(board):
        return timeit.timeit(
            lambda: bench_legal_moves(board),
            number=n,
            globals=locals(),
        )

    benchmark_template(1, n, bench, boards, False)


def benchmark_move(boards):
    n = 10000

    def bench(board):
        move = board.legal_moves()[0]
        return timeit.timeit(
            lambda: bench_move(board, move),
            number=n,
            globals=locals(),
        )

    benchmark_template(2, n, bench, boards, False)


def benchmark_evaluate(boards):
    n = 1000

    def bench_without_move(board):
        return timeit.timeit(
            lambda: bench_evaluate(board),
            number=n,
            globals=locals(),
        )

    def bench_with_move(board):
        move = board.legal_moves()[0]
        return timeit.timeit(
            lambda: bench_evaluate(board, move),
            number=n,
            globals=locals(),
        )

    benchmark_template(
        3,
        n,
        bench_without_move,
        boards,
        False,
    )
    benchmark_template(
        4,
        n,
        bench_with_move,
        boards,
        False,
    )


def benchmark_best_move(boards):
    n = 100
    depth = 1

    def bench(board):
        debug_info = DebugInfo(1)
        return timeit.timeit(
            lambda: bench_best_move(depth, board, debug_info),
            number=n,
            globals=locals(),
        )

    benchmark_template(5, n, bench, boards, True)


def benchmark():
    print("Initializing benchmarks...")
    boards_list = get_boards_list()
    prints_list = [
        "\n--------------- EARLY GAME BOARDS ---------------\n\n",
        "\n--------------- MID GAME BOARDS ---------------\n\n",
        "\n--------------- LATE GAME BOARDS ---------------\n\n",
    ]

    for i in range(len(boards_list)):
        print(prints_list[i])

        benchmark_to_fen(boards_list[i])
        benchmark_legal_moves(boards_list[i])
        benchmark_move(boards_list[i])
        benchmark_evaluate(boards_list[i])
        benchmark_best_move(boards_list[i])

    benchmark_dataframe.to_csv("benchmarks/benchmarks.csv", index=False)


if __name__ == "__main__":
    benchmark()
