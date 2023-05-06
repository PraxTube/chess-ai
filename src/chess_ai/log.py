import os
from datetime import datetime


main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

debug_info = {"nodes_searched": 0, "move_details": {}}


def get_log_file():
    date_str = datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
    log_file = f"log-{date_str}.txt"
    return log_file


def get_extensive_log_file():
    date_str = datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
    log_file = f"log-details-{date_str}.txt"
    return log_file


def append_log_file(last_move):
    with open(os.path.join(main_dir, "logs", log_file), "a") as f:
        move_str = f"{last_move.uci()}\n"
        f.writelines(move_str)


def append_extensive_log_file(board):
    with open(os.path.join(main_dir, "logs", extensive_log_file), "a") as f:
        reversed_moves = [x.uci() for x in debug_info["move_details"].values()]
        reversed_moves.reverse()
        moves = " ".join(reversed_moves)
        content = f"{board.fen()},{moves}\n"
        f.writelines(content)


log_file = get_log_file()
extensive_log_file = get_extensive_log_file()
