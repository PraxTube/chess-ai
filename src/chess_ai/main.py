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


def main():
    depth = args.depth
    debug_info = DebugInfo(depth)
    fen = args.fen
    _ = main_loop(depth, debug_info, turn_limit=-1, fen=fen)


if __name__ == "__main__":
    main()
