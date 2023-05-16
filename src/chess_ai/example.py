import chess
import chess.engine
import numpy as np

# we implement PEStos Evaluation method with 3 basic steps
# we have positional Awareness through piece square tables
# we have a timeline for midgame and endgame? -> maybe to advanced, where do we save the number of moves? next iteration?
# we have a materialist view

# store the pesto model weights for the different 
# mg stands for MIDGAME , eg stands for EDNGAME
mg_pawn_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    98, 134, 61, 95, 68, 126, 34, -11,
    -6, 7, 26, 31, 65, 56, 25, -20,
    -14, 13, 6, 21, 23, 12, 17, -23,
    -27, -2, -5, 12, 17, 6, 10, -25,
    -26, -4, -4, -10, 3, 3, 33, -12,
    -35, -1, -20, -23, -15, 24, 38, -22,
    0, 0, 0, 0, 0, 0, 0, 0,
]

eg_pawn_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    178, 173, 158, 134, 147, 132, 165, 187,
    94, 100, 85, 67, 56, 53, 82, 84,
    32, 24, 13, 5, -2, 4, 17, 17,
    13, 9, -3, -7, -7, -8, 3, -1,
    4, 7, -6, 1, 0, -5, -1, -8,
    13, 8, 8, 10, 13, 0, 2, -7,
    0, 0, 0, 0, 0, 0, 0, 0,
]

mg_knight_table = [
    -167, -89, -34, -49, 61, -97, -15, -107,
    -73, -41, 72, 36, 23, 62, 7, -17,
    -47, 60, 37, 65, 84, 129, 73, 44,
    -9, 17, 19, 53, 37, 69, 18, 22,
    -13, 4, 16, 13, 28, 19, 21, -8,
    -23, -9, 12, 10, 19, 17, 25, -16,
    -29, -53, -12, -3, -1, 18, -14, -19,
    -105, -21, -58, -33, -17, -28, -19, -23,
]

eg_knight_table = [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25, -8, -25, -2, -9, -25, -24, -52,
    -24, -20, 10, 9, -1, -9, -19, -41,
    -17, 3, 22, 22, 22, 11, 8, -18,
    -18, -6, 16, 25, 16, 17, 4, -18,
    -23, -3, -1, 15, 10, -3, -20, -22,
    -42, -20, -10, -5, -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64,
]

mg_bishop_table = [
    -29, 4, -82, -37, -25, -42, 7, -8,
    -26, 16, -18, -13, 30, 59, 18, -47,
    -16, 37, 43, 40, 35, 50, 37, -2,
    -4, 5, 19, 50, 37, 37, 7, -2,
    -6, 13, 13, 26, 34, 12, 10, -9,
    0, 15, 15, 15, 14, 27, 18, -18,
    4, 15, 16, 0, 7, 21, 33, -1,
    -19, -7, -37, -26, -36, -14, 2, -22,
]

eg_bishop_table = [
    -14, -21, -11, -8, -7, -9, -17, -24,
    -8, -4, 7, -12, -3, -13, -4, -14,
    2, -8, 0, 11, 2, 0, -5, -3,
    -3, 9, 12, 9, 14, 10, 3, 2,
    -6, 3, 13, 19, 7, 10, -3, -9,
    -12, 0, 0, 12, 10, 2, 0, -19,
    -14, -15, -2, -5, -1, -10, -20, -22,
    -22, -9, -23, -5, -9, -16, -5, -17,
]

mg_rook_table = [
    32, 42, 32, 51, 63, 9, 31, 43,
    27, 32, 58, 62, 80, 67, 26, 44,
    -5, 19, 26, 36, 17, 45, 61, 16,
    -24, -11, 7, 26, 24, 35, -8, -20,
    -36, -26, -12, -1, 9, -7, 6, -23,
    -45, -25, -16, -17, 3, 0, -5, -33,
    -44, -16, -20, -9, -1, 11, -6, -71,
    -19, -13, 1, 17, 16, 7, -37, -26,
]

eg_rook_table = [
    13, 10, 18, 15, 12, 12, 8, 5,
    11, 13, 13, 11, -3, 3, 8, 3,
    7, 7, 7, 5, 4, -3, -5, -3,
    4, 3, 13, 1, 2, 1, -1, 2,
    3, 5, 8, 4, -5, -6, -8, -11,
    -4, 0, -5, -1, -7, -12, -8, -16,
    -6, -6, 0, 2, -9, -9, -11, -3,
    -9, 2, 3, -1, -5, -13, 4, -20
]

mg_queen_table = [
    -28, 0, 29, 12, 59, 44, 43, 45,
    -24, -39, -5, 1, -16, 57, 28, 54,
    -13, -17, 7, 8, 29, 56, 47, 57,
    -27, -27, -16, -16, -1, 17, -2, 1,
    -9, -26, -9, -10, -2, -4, 3, -3,
    -14, 2, -11, -2, -5, 2, 14, 5,
    -35, -8, 11, 2, 8, 15, -3, 1,
    -1, -18, -9, 10, -15, -25, -31, -50
]

eg_queen_table = [
    -9, 22, 22, 27, 27, 19, 10, 20,
    -17, 20, 32, 41, 58, 25, 30, 0,
    -20, 6, 9, 49, 47, 35, 19, 9,
    3, 22, 24, 45, 57, 40, 57, 36,
    -18, 28, 19, 47, 31, 34, 39, 23,
    -16, -27, 15, 6, 9, 17, 10, 5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43, -5, -32, -20, -41
]

mg_king_table = [    -65,  23,  16, -15, -56, -34,   2,  13, 
                     29,  -1, -20,  -7,  -8,  -4, -38, -29,  
                     -9,  24,   2, -16, -20,   6,  22, -22,  
                     -17, -20, -12, -27, -30, -25, -14, -36,   
                     -49,  -1, -27, -39, -46, -44, -33, -51, 
                     -14, -14, -22, -46, -44, -30, -15, -27, 
                     1,   7,  -8, -64, -43, -16,   9,   8, 
                     -15,  36,  12, -54,   8, -28,  24,  14,]

eg_king_table = [  -74, -35, -18, -18, -11,  15,   4, -17,
                     -12,  17,  14,  17,  17,  38,  23,  11,
                      10,  17,  23,  15,  20,  45,  44,  13,
                    -8,  22,  24,  27,  26,  33,  26,   3, 
                    -18,  -4,  21,  24,  27,  23,   9, -11,
                     -19,  -3,  11,  21,  23,  16,   7,  -9,
                     -27, -11,   4,  13,  14,   4,  -5, -17, 
                       -53, -34, -21, -11, -28, -14, -24, -43,]


mg_peice_values = [82, 337, 365, 477, 1025, 0] # [pawn, knight, bishop, rook , queen , king ] I think I am not sure
eg_value = [94, 281, 297, 512, 936, 0]  #[pawn, knight, bishop, rook , queen , king ]

def pesto_evaluation(board, move=None ):
    score_to_return = 0

    if move:
        board.makeMove(move)
        fen_string = board.fen().split()[0]
        board.undoMove()
    else:
        fen_string = board.fen().split()[0]

    piece_chars = ["p", "b", "n", "r", "q", "k"]
    white_pieces = np.array([fen_string.count(x.upper()) for x in piece_chars])
    black_pieces = np.array([fen_string.count(x) for x in piece_chars])



def fen_to_array():
    import numpy as np

def fen_to_board(fen_str):
    # Split the FEN string into its components
    fen_parts = fen_str.split()
    fen_board = fen_parts[0]

    # Translate FEN board string to list of length 64
    board = np.zeros(64, dtype=np.int8)
    board_index = 0
    for char in fen_board:
        if char.isdigit():
            board_index += int(char)
        elif char == '/':
            pass
        else:
            piece = chess.Piece.from_symbol(char)
            piece_value = piece.piece_type
            if piece.color == chess.WHITE:
                piece_value = -piece_value
            board[board_index] = piece_value
            board_index += 1

    return board

