import os
from io import StringIO
import timeit
import contextlib
import pandas as pd

from chess_ai import chess_engine as chess
from chess_ai import move
from chess_ai import evaluate


script_dir = os.path.dirname(os.path.abspath(__file__))
benchmark_file = os.path.join(script_dir, "boards_and_moves.txt")
benchmark_dataframe = pd.DataFrame(
    columns=["Game Stage", "Type", "Total", "Average", "Valid Moves", "Fen"]
)
stage = ["Early", "Mid", "Late"]


def benchmark_to_dataframe(
    stage_index, msg, total_time, average_time, valid_moves, fen
):
    row_data = {
        "Game Stage": stage[stage_index],
        "Type": msg,
        "Total": total_time,
        "Average": average_time,
        "Valid Moves": valid_moves,
        "Fen": fen,
    }
    benchmark_dataframe.loc[len(benchmark_dataframe)] = row_data


def suppress_prints():
    return StringIO()


def get_boards(file):
    with open(os.path.join(script_dir, file), "r") as f:
        content = f.readlines()
        boards = [chess.GameState(x) for x in content]
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
            board.getValidMoves()


def bench_move(board, move):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            board.makeMove(move)
            board.undoMove()


def bench_best_move(depth, board):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            move.next_move(depth, board)


def bench_evaluate(board, move=None):
    with contextlib.redirect_stdout(suppress_prints()):
        with contextlib.redirect_stderr(suppress_prints()):
            evaluate.evaluate_board(board, move)


def benchmark_template(msg, n, result_func, boards, use_seconds, stage_index):
    print(f"\n==========\n{msg}\n==========\n")
    csv_msg = msg
    for board in boards:
        result = result_func.__call__(board)

        if use_seconds:
            msg = "Total: {}s, Average: {}ms - {} - {}"
            total_time = round(result, 4)
            average_time = round(result / n * 1000, 2)
        else:
            msg = "Total: {}ms, Average: {}µs - {} - {}"
            total_time = round(result * 1000, 4)
            average_time = round(result / n * 1000 * 1000, 2)

        print(
            msg.format(
                total_time,
                average_time,
                len(board.getValidMoves()),
                board.fen(),
            )
        )
        benchmark_to_dataframe(
            stage_index,
            csv_msg,
            total_time,
            average_time,
            len(board.getValidMoves()),
            board.fen(),
        )


def benchmark_to_fen(boards, stage_index):
    n = 10000

    def bench(board):
        return timeit.timeit(
            lambda: bench_to_fen(board),
            number=n,
            globals=locals(),
        )

    benchmark_template(
        "Benchmark to fen string conversion", n, bench, boards, False, stage_index
    )


def benchmark_legal_moves(boards, stage_index):
    n = 10000

    def bench(board):
        return timeit.timeit(
            lambda: bench_legal_moves(board),
            number=n,
            globals=locals(),
        )

    benchmark_template(
        "Benchmark legal moves generation", n, bench, boards, False, stage_index
    )


def benchmark_move(boards, stage_index):
    n = 10000

    def bench(board):
        move = board.getValidMoves()[0]
        return timeit.timeit(
            lambda: bench_move(board, move),
            number=n,
            globals=locals(),
        )

    benchmark_template("Benchmark making moves", n, bench, boards, False, stage_index)


def benchmark_evaluate(boards, stage_index):
    n = 1000

    def bench_without_move(board):
        return timeit.timeit(
            lambda: bench_evaluate(board),
            number=n,
            globals=locals(),
        )

    def bench_with_move(board):
        move = board.getValidMoves()[0]
        return timeit.timeit(
            lambda: bench_evaluate(board, move),
            number=n,
            globals=locals(),
        )

    benchmark_template(
        "Benchmark evaluate board WITHOUT move",
        n,
        bench_without_move,
        boards,
        False,
        stage_index,
    )
    benchmark_template(
        "Benchmark evaluate board WITH move",
        n,
        bench_with_move,
        boards,
        False,
        stage_index,
    )


def benchmark_best_move(boards, stage_index):
    n = 100

    def bench(board):
        return timeit.timeit(
            lambda: bench_best_move(1, board),
            number=n,
            globals=locals(),
        )

    benchmark_template(
        "Benchmark best move generation", n, bench, boards, True, stage_index
    )


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

        benchmark_to_fen(boards_list[i], i)
        benchmark_legal_moves(boards_list[i], i)
        benchmark_move(boards_list[i], i)
        benchmark_evaluate(boards_list[i], i)
        benchmark_best_move(boards_list[i], i)

    benchmark_dataframe.to_csv("benchmarks/benchmarks.csv")
    benchmark_dataframe.to_latex("benchmarks/benchmarks.tex", index=False)


if __name__ == "__main__":
    benchmark()
