import argparse

from chess_ai.play import main_loop
from chess_ai.log import DebugInfo

parser = argparse.ArgumentParser(description="Chess AI that uses alpha-beta search.")
parser.add_argument(
    "-d",
    "--depth",
    action="store",
    type=int,
    default=3,
    help="The depth for the alpha-beta tree search",
)
parser.add_argument(
    "-f",
    "--fen",
    action="store",
    type=str,
    default="",
    help="The start fen, default is the start position",
)
args = parser.parse_args()


def game_over_message(result, fen):
    if result == -1:
        print("Game not concluded yet. Stoped after turn limit was reached.")
        return

    if result == 0:
        print("\n\nSTALEMATE!\n---\nNeither side won!")
    else:
        winner = "White - Max" if result == 1 else "Black - Min"
        print(f"\n\nCHECKMATE!\n---\nThe winner is {winner}!")
    print(f"FEN:\n{fen}")


def main():
    depth = args.depth
    debug_info = DebugInfo(depth)
    fen = args.fen
    result, end_board = main_loop(depth, debug_info, turn_limit=-1, fen=fen)
    game_over_message(result, end_board.fen())


if __name__ == "__main__":
    main()
