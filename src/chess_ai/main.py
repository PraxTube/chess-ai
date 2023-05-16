import argparse

from chess_ai.play import main_loop

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
    main_loop(args.depth)


if __name__ == "__main__":
    main()
