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
args = parser.parse_args()


def main():
    depth = args.depth
    debug_info = DebugInfo(depth)
    main_loop(depth, debug_info)


if __name__ == "__main__":
    main()
