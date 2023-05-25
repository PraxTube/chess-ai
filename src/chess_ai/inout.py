from chess_ai.evaluate import evaluate_board


def print_board(board, best_move, debug_info):
    evaluation_ratio = evaluate_board(board)
    boards_searched = debug_info.nodes_searched
    move_details = debug_info.move_details
    print("\n------------\n")
    print(board)
    print(f"\nCurrent Evaluation of the board is: {evaluation_ratio}")
    print(f"Best move has evaluation of {best_move}")
    print(f"Number of boards searched: {boards_searched}")
    print(f"Move Details:\n{move_details}")
