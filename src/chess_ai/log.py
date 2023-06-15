import os
from datetime import datetime


class DebugInfo:
    def __init__(self, depth):
        self.nodes_searched = 0
        self.move_details = {}
        for i in range(1, depth):
            self.move_details[i] = None

        self.setup_logs_dir()
        self.setup_files()

    def reset_nodes(self):
        self.nodes_searched = 0

    def increment_nodes(self):
        self.nodes_searched += 1

    def setup_logs_dir(self):
        main_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        os.makedirs(os.path.join(main_dir, "logs"), exist_ok=True)
        self.logs_dir = os.path.join(main_dir, "logs")

    def setup_files(self):
        date_str = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = os.path.join(self.logs_dir, f"log-{date_str}.txt")
        self.extensive_log_file = os.path.join(
            self.logs_dir, f"log-details-{date_str}.txt"
        )


def append_log_file(last_move, debug_info):
    with open(debug_info.log_file, "a") as f:
        move_str = f"{last_move.coordinate()}\n"
        f.writelines(move_str)


def append_extensive_log_file(board, debug_info):
    with open(debug_info.extensive_log_file, "a") as f:
        reversed_moves = [x for x in debug_info.move_details.values()]
        reversed_moves.reverse()
        moves = " ".join(reversed_moves)
        content = f"{board.fen()},{moves}\n"
        f.writelines(content)
