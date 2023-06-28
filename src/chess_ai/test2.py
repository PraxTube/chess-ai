import random
import numpy as np
import  chess_engine as chess
import operator

# TODO: board = board.board für  alles funktionen umändern!

# TODO : Dokumentation schreiben mit quellen drin

# TODO : backward pawn implementation and test

# TODO : GamePhase Interpolation


# implementation after fruit -> uses the contact squares 
# different number of attacker have different weightings 
def evaluate_king_danger(board, white_to_move):

    if white_to_move:
        king_piece = 6
    else:
        king_piece = -6
    
    moves = []
    try:
        king_pos = board.find_piece(king_piece)
    except:
        print("Where's the king?")

    board.king_moves(king_pos[0], king_pos[1], moves)

    # für alle end - squares , schaun ob es im check ist

    attack_count = 0
    for move in moves:
        if board.square_under_attack(move.end_row, move.end_col) == True:
            attack_count += 1
        else:
            continue
    
    if white_to_move:
        return (attack_count) * 20
    else : return -((attack_count) * 20)

# add a randomness to a given state of the board in the range of [-30, 30]

def add_randomness() -> int:

    start_range = -30
    end_range = 30
    return random.randint(start_range, end_range)

# queen : 9 , rook : 5, bishop : 3 , knight : 3 , pawn 1
# these values come from dissertation wolfgang kantschik
#  teh simple equation for material differece: material[white_to_move] - material [not white_to_move]
# https://www.chessprogramming.org/Material#Material_Balance
# 40 points punishment if your material is less than from the opponent
def material_evaluation(board, white_to_move):
    piece_val_dic_white = {
        1 : 1, # white Pawn
        2 : 3 , # white knight
        3 : 3 , # white bishop
        4 : 5, # white rook
        5: 9 # white queen
    }

    piece_val_dic_black = {
        -1 : 1, # black Pawn
        -2 : 3 , # black knight
        -3 : 3 , # black bishop
        -4 : 5, # black rook
        -5: 9 # black queen
    }

    mat_score_black = 0
    mat_score_white = 0

    board = board.board
    for row in range(len(board)):
        for col in range(len(board[row])):

            if board[row][col] in piece_val_dic_black:
                mat_score_black += piece_val_dic_black[board[row][col]]
            elif board[row][col] in piece_val_dic_white:
                mat_score_white += piece_val_dic_white[board[row][col]]
            else:
                continue
         

    if white_to_move and (mat_score_white - mat_score_black) > 0 :
        return 40
    elif white_to_move and (mat_score_white - mat_score_black) < 0:
        return - 40
    elif not white_to_move and (mat_score_black - mat_score_white) > 0:
        return - 40
    elif not white_to_move and (mat_score_black - mat_score_white) < 0:
        return 40
    elif mat_score_white == mat_score_black:
        return 0








    
# https://www.chessprogramming.org/King_Safety#Square_Control
# gonna implement pawn shield 
# not gonna implement it for castling, since we think its so relevant for king of the hills
# pawn shield: abzug wenn auf den drei linien vor dem könig, keine bauner sind
def evaluate_king_shelter(board, white_to_move):
    if white_to_move:
        pawn_piece = 1
        king_piece = 6
    else:
        pawn_piece = -1
        king_piece = -6

    # check if there are 3 pawns on every adjacent king line

    try:
        king_pos = board.find_piece(king_piece)
    except:
        print("was los?")
    
    tboard = np.array(board.board).T.tolist()

    my_list = range(king_pos[1] -1, king_pos[1] +2 )
    print(king_pos[1], "-----", str(my_list))
    
    count = 0
    for line in my_list:
        if pawn_piece not in tboard[line] :
            count += 1
        else:
            continue

    if white_to_move:
        return count * (-20)
    else: return count * 20


        

# punish pawns : In chess, an isolated pawn is a pawn that has no friendly pawn on an adjacent file
# function punish_pawns_not right_aligned is something similar
def punish_isolated_pawns(board, white_to_move):

    if white_to_move:
        pawn_piece = 1
        enemy_piece = -1
    else:
        pawn_piece = -1
        enemy_piece = 1
    
    alpha= 1

    tboard =  np.array(board.board).T.tolist()
    print(tboard)

    count = 0

    for row in range(len(tboard)):

        if row == 0 and pawn_piece  in tboard[row] and pawn_piece not in tboard[row + alpha]:
            count += 1
        elif row == 7 and pawn_piece  in tboard[row] and pawn_piece not in tboard[row - alpha]:
            count += 1
        elif pawn_piece  in tboard[row] and pawn_piece not in tboard[row - alpha] and pawn_piece not in tboard[row + alpha]:
            count += 1
        else:
            continue
    
    if white_to_move:
        return -count * 20
    else:
        return  count *20

# a backward pawn cannot advance without being captured and has no support from adjacent pawns
# also after stockfish chess engine a backward pawn must be behind all pawns of the same color
def punish_backward_pawns(board, white_to_move):

    if white_to_move:
        pawn_piece = 1
        dir_step = -1
        max_row = 8
    else:
        pawn_piece = -1
        dir_step = 1
        max_row = 0
    
    # we do not look at the outside squares
    rows = range(1,7)
    cols = range(1,7)

    back_ward_pawn_count = 0
    
    for row in rows:
        for col in cols:

            if board[row][col] == pawn_piece:
                # check if there if one step further would be under attack
                if board.square_under_attack(board[row + dir_step] [col]):
                    # check if there are adjacent pawns that that can support you
                    if board[row][col +1] == pawn_piece or board[row][col-1] == pawn_piece:
                        continue
                    else:
                        back_ward_pawn_count +=1
                else:
                    continue
            else:
                continue
        
    if white_to_move:
        return back_ward_pawn_count * -20
    else:
        return back_ward_pawn_count *20







# bonus wenn gegnerischer könig auf dem 8. rang ist und unsere queen auf dem 7. ist, 20 , nochmal mehr im Endgame
def queen_on_seventh_rank(board, white_to_move):
    score_to_return = 0

    if white_to_move:
        piece = 5
        enemy_king = -6
        seventh_rank = 1
        eight_rank = 0
    else :
        piece= -5
        enemy_king = 6
        seventh_rank = 6
        eight_rank = 7
    
    try:
        king_pos = board.find_piece(enemy_king) # hier nochmal überprüfen, ob das geht
        queen_pos = board.find_piece(piece)
        
    except:
        return 0

    board = board.board

    if king_pos[0] == eight_rank and queen_pos[0] == seventh_rank:                                          
        score_to_return = 20
    
    if white_to_move:
        return score_to_return
    else:
        return -score_to_return

#bonus wenn gegnerischer könig auf dem 8. rang ist und unser turm auf dem 7. , 15 , nochmal mehr im endgame
def rooks_on_seventh_rank(board, white_to_move):


    score_to_return = 0

    if white_to_move:
        piece = 4
        enemy_king = -6
        seventh_rank = 1
        eight_rank = 0
    else :
        piece= -4
        enemy_king = 6
        seventh_rank = 6
        eight_rank = 7
    
    try:
        king_pos = board.find_piece(enemy_king) # hier nochmal überprüfen, ob das geht
        
    except:
        return 0

    board = board.board

    rook_count = 0

    for i in board[seventh_rank]:
        if i == enemy_king:
            rook_count += 1

    if king_pos[0] == eight_rank and rook_count > 0:                                          
        score_to_return = rook_count * 15
    
    if white_to_move:
        return score_to_return
    else:
        return -score_to_return


#TODO hier die funktion umschreiben   

def bishop_mobility(board, white_to_move):

    if white_to_move:
        piece = 3
    else :
        piece = -3

    positions = []

    try:

        positions.append(board.find_piece(piece))   # weiß nicht, ob das soa uh klappt 
        positions.append(board.find_piece(piece))

    except ValueError:

        print("Gibt anscheinend nur noch einen")


    moves = []
    for pos in positions:
        board.bishop_moves(pos[0], pos[0], moves)
    
    score_to_return = len(moves) *3  #linear evaluation

    if white_to_move:
        return score_to_return
    else:
        return - score_to_return

# erweitertes zentrum 4x 4 felder in der mitte
# bstraft wenn > 2 eigene bauern auf dem jeweiligen feld des läufers stehen
# summe der indizes gerade -> weißes feld, ungerade -> schwarzes feld
# pro trapped bishop, wird so viel bestraft: 20
def trapped_bishops(board, white_to_move):

    # position vom schwarzen und weißen läufer finden
    #
    board = board.board

    score_to_return = 0

    if white_to_move:
        piece = 3
        pawn_piece = 1
    else :
        piece = -3
        pawn_piece = -1
    
    pawn_piece_count_black_square = 0
    pawn_piece_count_white_square = 0
    
    black_square_bishop = None
    white_sqare_bishop = None

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == piece and (i + j) % 2 == 0 :
                white_sqare_bishop = 1
            elif board[i][j] == piece and (i + j) % 2 == 1: 
                black_square_bishop = 1
            elif board[i][j] == pawn_piece and (i + j) % 2 == 0 and 2 <= i <= 5 and 2 <= j <= 5 :
                pawn_piece_count_white_square += 1
            elif board[i][j] == pawn_piece and (i + j) % 2 == 1 and 2 <= i <= 5 and 2 <= j <= 5:
                pawn_piece_count_black_square += 1
            else:
                pass
    
    
    if black_square_bishop == 1 and pawn_piece_count_black_square > 2 :
        score_to_return += 20
    elif white_sqare_bishop == 1 and pawn_piece_count_white_square > 2 :
        score_to_return += 20
    else:
        pass

    if white_to_move:
        return score_to_return
    else:
        return - score_to_return



def rook_moobility(board, white_to_move):
    if white_to_move:
        piece = 4
    else :
        piece = -4

    positions = []

    try:

        positions.append(board.find_piece(piece))
        positions.append(board.find_piece(piece))

    except ValueError:

        print("Gibt anscheinend nur noch einen")


    moves = []
    for pos in positions:
        board.bishop_moves(pos[0], pos[0], moves)
    
    score_to_return = len(moves) *3  #linear evaluation

    if white_to_move:
        return score_to_return
    else:
        return - score_to_return



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
