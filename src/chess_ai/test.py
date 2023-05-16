import chess
import pprint
import numpy as np

board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")

# mg_peice_values = [82, 337, 365, 477, 1025, 0] [pawn, knight, bishop, rook , queen , king ] I think I am not sure
# Implementation without changing the gamestate, just logic of positional awareness
piece_values = {
    'p': 82,
    'n': 337,
    'b': 365,
    'r': 477,
    'q': 1025,
    'k': 0 # nicht ganz sicher, ob das so gewollt ist?? werte sind ja schnell ausgetaucht

}

piece_tables ={
    'p': [0, 0, 0, 0, 0, 0, 0, 0,98, 134, 61, 95, 68, 126, 34, -11,-6, 7, 26, 31, 65, 56, 25, -20,-14, 13, 6, 21, 23, 12, 17, -23,-27, -2, -5, 12, 17, 6, 10, -25,-26, -4, -4, -10, 3, 3, 33, -12,-35, -1, -20, -23, -15, 24, 38, -22,0, 0, 0, 0, 0, 0, 0, 0],
    'n': [
    -167, -89, -34, -49, 61, -97, -15, -107,
    -73, -41, 72, 36, 23, 62, 7, -17,
    -47, 60, 37, 65, 84, 129, 73, 44,
    -9, 17, 19, 53, 37, 69, 18, 22,
    -13, 4, 16, 13, 28, 19, 21, -8,
    -23, -9, 12, 10, 19, 17, 25, -16,
    -29, -53, -12, -3, -1, 18, -14, -19,
    -105, -21, -58, -33, -17, -28, -19, -23
],
    'b':[
    -29, 4, -82, -37, -25, -42, 7, -8,
    -26, 16, -18, -13, 30, 59, 18, -47,
    -16, 37, 43, 40, 35, 50, 37, -2,
    -4, 5, 19, 50, 37, 37, 7, -2,
    -6, 13, 13, 26, 34, 12, 10, -9,
    0, 15, 15, 15, 14, 27, 18, -18,
    4, 15, 16, 0, 7, 21, 33, -1,
    -19, -7, -37, -26, -36, -14, 2, -22
],
    'r':[
    32, 42, 32, 51, 63, 9, 31, 43,
    27, 32, 58, 62, 80, 67, 26, 44,
    -5, 19, 26, 36, 17, 45, 61, 16,
    -24, -11, 7, 26, 24, 35, -8, -20,
    -36, -26, -12, -1, 9, -7, 6, -23,
    -45, -25, -16, -17, 3, 0, -5, -33,
    -44, -16, -20, -9, -1, 11, -6, -71,
    -19, -13, 1, 17, 16, 7, -37, -26
],
    'q':[
    -28, 0, 29, 12, 59, 44, 43, 45,
    -24, -39, -5, 1, -16, 57, 28, 54,
    -13, -17, 7, 8, 29, 56, 47, 57,
    -27, -27, -16, -16, -1, 17, -2, 1,
    -9, -26, -9, -10, -2, -4, 3, -3,
    -14, 2, -11, -2, -5, 2, 14, 5,
    -35, -8, 11, 2, 8, 15, -3, 1,
    -1, -18, -9, 10, -15, -25, -31, -50
],

    'k': [    -65,  23,  16, -15, -56, -34,   2,  13, 
                     29,  -1, -20,  -7,  -8,  -4, -38, -29,  
                     -9,  24,   2, -16, -20,   6,  22, -22,  
                     -17, -20, -12, -27, -30, -25, -14, -36,   
                     -49,  -1, -27, -39, -46, -44, -33, -51, 
                     -14, -14, -22, -46, -44, -30, -15, -27, 
                     1,   7,  -8, -64, -43, -16,   9,   8, 
                     -15,  36,  12, -54,   8, -28,  24,  14]
}

# translates
# nur kleine chars als input parameter
def fen_to_board(fen, color, piece_char):
    board = [0] * 64
    ranks = fen.split()[0].split('/')
    for x in ranks:
        print(x)

    if color == 'w':
        piece_char = piece_char.upper()

    for rank_idx, rank in enumerate(ranks):
        file_idx = 0
        for char in rank:
            if char.isnumeric():
                file_idx += int(char)
            else:
                if char == piece_char:
                    board[rank_idx*8+file_idx] = piece_values[piece_char.lower()]
                file_idx += 1

    return board



def evaluate(board, move=None):

    score_to_return = 0

    if move:
        board.makeMove(move)
        fen_string = board.fen().split()[0]
        board.undoMove()
    else:
        fen_string = board.fen().split()[0]

    
    
    color_chars = ['w', 'b']
    piece_chars = ["p", "b", "n", "r", "q", "k"]

    # reihenfolge: zuerst weiß alle pieces durch dann , schwarz
    list_of_lists = []

    # filling the list of list, having for every color and every piece a python list , with the weighted materialistic value on the right index
    for cchar in color_chars:
        for pchar in piece_chars:
            list_of_lists.append(fen_to_board(fen_string, cchar, pchar))
    
      # len should be 12
    
    # now using matrixmultiplication using the piece_square tables
    for n in range(len(list_of_lists)):
        A = np.array(list_of_lists[n])
        if n == 0 or n == 6:
            B = np.array(piece_tables['p'])
        elif n == 1 or n == 7:
             B = np.array(piece_tables['n'])
        elif n == 2 or n == 8:
            B = np.array(piece_tables['b'])
        elif n == 3 or n == 9:
             B = np.array(piece_tables['r'])
        elif n == 4 or n == 10:
            B = np.array(piece_tables['q'])
        elif n == 5 or n == 11:
            B = np.array(piece_tables['k'])
        else:
            print(" was geht jetzt ab??")

        # nicht ganz sicher bei der Zusammenrechnung der Werte
        if n >= 0 and n <= 5:
            # weil wir aus sicht von weiß spielen?
            score_to_return += np.dot(A,B)
        else:
            # weil wir schwarz minimieren müssen?
            score_to_return -= np.dot(A,B)
    
    return score_to_return

    

x = evaluate(board)
print(x)
 


