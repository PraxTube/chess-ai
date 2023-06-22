
import numpy as np
import  chess_ai.chess_engine as chess
import operator


# weiß wird miximiert
# schwaz wird minimiert
# bestrafung für einen läufer in anfangsposition 
def punish_bishop_on_SP(board, white_to_move):

    score = 0
    if white_to_move:
        if board[7][2] == 3 :
            score -=15
        if board[7][5] == 3:
            score -= 15
        return score
        
    else:
        if board[0][2] == -3 :
            score +=15
            
        if board[0][5] == -3:
            score += 15
    
        return score
    

#Bonus, wenn beide Läufer vorhanden sind [20]

def bonus_both_bishops(board,  white_to_move):
    count = 0

    if white_to_move:
        piece = 3
    else:
        piece = -3

    for x in range(len(board)):
        for i in range(len(board[x])):
            if board[x][i] == piece:
                count += 1

    if white_to_move and count ==2: return  20 
    elif not white_to_move and count == 2 : return -  20 
    else : return 0

#Bestrafung für einen Bauern der keinen Bauern auf den Nachbarlinien hat, der näher an der ersten Reihe des Gegners ist [15]
# --> strafe für einen bauern der keinen anderen bauern deckt?
# weder links noch rechts einen anderen schräg vor ich hat
def punish_for_pawns_not_right_aligned(board, white_to_move):
    if white_to_move:
        piece = 1
        range_test = [6, 5] # only these are the rows in which I will evaluate this feature
        alpha = -1
    else :
        piece = -1
        range_test = [1,2]
        alpha = 1

    score = 0
    for row in range_test:
        for col in range(len(board[row])):
            a = board[row][col]
            if a == 0 : pass
            else:
                if col == 0 :
                    
                    if board[row][col] == piece and board[row + alpha][col+1] == piece:
                        pass
                    else:
                        score += 15
                
                elif col == 7:

                    if board[row][col] == piece and board[row + alpha][col-1] == piece:
                        pass
                    else:
                        score += 15

                else:

                    if board[row][col] == piece and (board[row + alpha][col-1] == piece or board[row + alpha][col+1] == piece):
                        pass
                    else:
                        score +=15

    
    if white_to_move:
        # minus score weil es für den weißne maximierneden spieler eine bestrafung ist
        return -score
    else :
        # positiver score weil es für den schwarzen minimierenden eine spieler eine positive zahl eine bestrafung ist
        return  score
     

# Bonus für einen Bauern, wenn er in der Nähe der ersten Reihe des Gegners ist (Promotionsmöglichkeit) [300]
def pawn_promotion_poss(board, white_to_move):
    # vorlezte reihe
    if white_to_move:
        piece = 1
        row = 1
        alpha = -1
    else:
        piece = -1
        row = 6
        alpha = 1
    
    count = 0
    for col in range(len(board[row])):
        if board[row][col] == piece and board[row+alpha][col] == 0 :
            count += 1
    
    if white_to_move:
        return (300 *count)
    else:
        return -(300 *count)


#Bestrafung, wenn die Möglichkeit einer Rochade vergeben wurde [20]


            




# bonus für einen bauern, der das Zentrum des schachbretts erreicht hat
def bonus_pawns_in_centre(board, white_to_move):
# slice the centre of the map , die mittleren 16 felder
    centre = [board[x][2:6] for x in range(2,6)]
    if white_to_move:
        piece = 1
    else :
        piece = -1

    x = 0

    for i in range(len(centre)):
        for j in range(len(centre[i])):
            if centre[i][j] == piece:
                x += 15

    if white_to_move:
        return x
    else:
        return -x  

#Bestrafung, wenn zwei Bauern auf der gleichen Linie stehen [30]
def punish_pawns_same_line(board, white_to_move):
    if white_to_move:
        piece = 1
    else :
        piece = -1
    
    new_board = np.array(board)
    tboard = new_board.transpose()

    x = 0
    for i in range(len(tboard)):
        count = 0
        for j in range(len(tboard[i])):
            if tboard[i][j] == piece:
                count += 1
        
        if count >= 2:
            x += 30

    if white_to_move:
        return -x
    else :
        return x

# Bonus für einen Bauern, der auf beiden Nachbarlinien keinen gegnerischen Bauern hat [20]
# hier auch auf die äußeren linien achten
def bonus_paws_neighbor_lines(board, white_to_move):
    
    new_board = np.array(board)
    tboard = new_board.transpose()
    score = 0
    if white_to_move:
        op_pawn_piece = -1
        my_pawn = 1
    else :
        op_pawn_piece = 1
        my_pawn = -1
    
    for x in range(0, len(tboard)):
        count_op_pawn = 0
        count_my_pawn = 0
        if x == 0:
            for i in range(0 , len(tboard[x])):
                if tboard[x+1][i] == op_pawn_piece:
                    count_op_pawn += 1
                elif tboard[x][i] == my_pawn:
                    count_my_pawn +=1

        elif x == 7:
            for i in range(0 , len(tboard[x])):
                if tboard[x-1][i] == op_pawn_piece:
                    count_op_pawn += 1
                elif tboard[x][i] == my_pawn:
                    count_my_pawn +=1
        else:
            for i in range(0, len(tboard[x])):
                if tboard[x-1][i] == op_pawn_piece or tboard[x+1][i] == op_pawn_piece:
                    count_op_pawn += 1
                elif tboard[x][i] == my_pawn:
                    count_my_pawn +=1

        if count_op_pawn == 0 and count_my_pawn >= 1:
            score += 20

        
    if white_to_move : return score
    else : return - score


#Bonus für den Turm, wenn er auf einer halboffenen Linie steht [15]
#  auf halboffenen befinden sich nur Bauern einer Farbe
def bonus_for_Rook_halfopen_lines(board, white_to_move):
    if white_to_move:
        rook_piece = 4
    else :
        rook_piece = -4
    
    white_pawn = 1
    black_pawn = -1
    score_to_return = 0
    new_board = np.array(board)
    tboard = new_board.transpose()
    for i in range(len(tboard)):
        wcount = 0
        bcount = 0
        for j in range(len(tboard[i])):
            if tboard[i][j] == white_pawn:
                wcount +=1
            elif tboard[i][j] == black_pawn:
                bcount +=1
            
        if rook_piece in tboard[i] and (operator.xor(wcount == 0 , bcount == 0)):
            score_to_return += 15
    
    if white_to_move:
        return score_to_return
    else :
        return - score_to_return


 #Bonus für den Turm, wenn er auf einer offenen Linie steht [15]
#Auf offenen Linien befindet sich kein Bauer
def bonus_for_Rook_open_lines(board, white_to_move):
    if white_to_move:
        rook_piece = 4
    else :
        rook_piece = -4
    
    white_pawn = 1
    black_pawn = -1
    score_to_return = 0

    new_board = np.array(board)
    tboard = new_board.transpose()
    for i in range(len(tboard)):
        wcount = 0
        bcount = 0
        for j in range(len(tboard[i])):
            if tboard[i][j] == white_pawn:
                wcount +=1
            elif tboard[i][j] == black_pawn:
                bcount +=1
            
        if rook_piece in tboard[i] and wcount == 0 and bcount == 0:
            score_to_return += 15
    
    if white_to_move:
        return score_to_return
    else :
        return - score_to_return

 #Bonus für den Turm, falls er von dem anderen Turm gedeckt wird [15]
def bonus_Rook_covered_rook(board, white_to_move):
    if white_to_move:
        rook_piece = 4
    else :
        rook_piece = -4
    
    
    # [row, col , row, col]
    places = []
    data = board.board
    for row in range(len(data)):
            for col in range(len(data[0])):
                if data[row][col] == rook_piece:
                   places.append(row)
                   places.append(col)
    # kleiner check ob es überhaupt 2 türme noch im spiel gibt
    if len(places) <= 2:
        return 0
    else:
        moves = []
        board.rook_moves(places[0], places[1], moves)
        board.rook_moves(places[2], places[3], moves)
    c = 0
    for move in moves:
        #end_square[0] ist end_row, 
        if move.end_col in places and move.end_row in places:
            c+=1
            
    
    if white_to_move and c >=1:return 30
    elif not white_to_move and c >=1: return - 30
    else: return 0



def evaluate_pawn_features(board, white_to_move):
    score = 0
    score += pawn_promotion_poss(board, white_to_move)
    score += punish_pawns_same_line(board, white_to_move)
    score += evaluate_pawn_features(board, white_to_move)
    score += bonus_pawns_in_centre(board, white_to_move)
    score += punish_for_pawns_not_right_aligned(board, white_to_move)

    return score

def evaluate_bishop_features(board, white_to_move):

    score = 0
    score += punish_bishop_on_SP(board, white_to_move)
    score += bonus_both_bishops(board, white_to_move)

def evaluate_rook_features(board, white_to_move):
    
    score = 0
    score += bonus_Rook_covered_rook(board, white_to_move)
    score += bonus_for_Rook_halfopen_lines(board , white_to_move)
    score += bonus_for_Rook_open_lines(board, white_to_move)

        
        

def evaluate_board(board, white_to_move, move=None):
    
    score_to_return = 0
    if move:
        board.makeMove(move)
        fen_string = board.fen().split()[0]
        board.undoMove()
    else:
        fen_string = board.fen().split()[0]

    score_to_return += evaluate_pawn_features(board, white_to_move)
    score_to_return += evaluate_rook_features(board, white_to_move)
    score_to_return += evaluate_bishop_features(board, white_to_move)

    return score_to_return
