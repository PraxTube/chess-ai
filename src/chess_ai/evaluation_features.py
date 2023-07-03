import random
import numpy as np
import operator



def count_pawns (game_board, white_to_move):
    if white_to_move:
        pawn_piece = 1
    else:
        pawn_piece = -1
    
    pawn_count = 0
    for row in range(len(game_board)):
        for col in range(len(game_board[row])):
            if game_board[row][col] == pawn_piece:
                pawn_count +=1

    return pawn_count


def game_interpolation_is_endgame(board, white_to_move):

    game_board = board.board

    queen_missing = False

    dangerous_positions = [(2,2), (2,3), (2,4), (2,5), (3,2), (4,2), (5,2), (5,3), (5,4), (5,5), (3,5), (4,5)]
    central_king_location = False

    if board.white_king_location in dangerous_positions or board.black_king_location in dangerous_positions:
        central_king_location = True

    try:
        a = board.find_piece(5)
        b = board.find_piece(-5)
    except ValueError:
        queen_missing = True

    if (count_pawns(game_board, True) <= 4 or count_pawns(game_board, False) and queen_missing) or central_king_location:
        return True
    else :
        return False



# implementation after fruit -> uses the contact squares 
# we only use one score for every attacker
def get_king_contact_squares(row, col):
    
    contact_squares = []

    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if 0 <= i < 8 and 0 <= j < 8 and (i, j) != (row, col):
                contact_squares.append((i, j))

    return contact_squares


def evaluate_king_danger(board, white_to_move):

    if white_to_move:
        king_piece = 6
    else:
        king_piece = -6
    
    try:
        king_pos = board.find_piece(king_piece)
    except:
        print("Where's the king?")

    moves = get_king_contact_squares(king_pos[0], king_pos[1])

    # für alle end - squares , schaun ob es under attack ist

    attack_count = 0
    for move in moves:
        if board.square_under_attack(move[0], move[1]) == True:
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
# not gonna implement it for castling, since we think its not so relevant for king of the hills
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
def punish_isolated_pawns(board, white_to_move):

    if white_to_move:
        pawn_piece = 1
    else:
        pawn_piece = -1
    
    alpha= 1

    tboard =  np.array(board.board).T.tolist()
    

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
      
    else:
        pawn_piece = -1
        dir_step = 1
       
    # find the rank with the last pawn on the side

    game_board = board.board

    pawn_rows = []

    for row in range(len(game_board)):
        if pawn_piece in game_board[row]:
            pawn_rows.append(row)

    if white_to_move:
        result_row = max(pawn_rows)
    else: result_row = min(pawn_rows)

    back_ward_pawn_count= 0

    # check backward pawn conditions, they cannot have support from other files
    for col in range(len(game_board)):
        if game_board[result_row][col] == pawn_piece  and  board.square_under_attack(row + dir_step ,col):
            back_ward_pawn_count +=1
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

 

def bishop_mobility(board, white_to_move):

    if white_to_move:
        piece = 3
    else :
        piece = -3

    positions = []

    game_board = board.board

    for row in range(len(game_board)):
        for col in range(len(game_board[row])):
            if game_board[row][col] == piece:
                positions.append((row, col))


    moves = []
    for pos in positions:
        board.bishop_moves(pos[0], pos[1], moves)
    
    score_to_return = len(moves) *3  #linear evaluation

    if white_to_move:
        return score_to_return
    else:
        return - score_to_return

# erweitertes zentrum 4x 4 felder in der mitte
# bstraft wenn > 2 gegnerische bauern auf dem jeweiligen feld des läufers stehen
# summe der indizes gerade -> weißes feld, ungerade -> schwarzes feld
# pro trapped bishop, wird so viel bestraft: 20
def trapped_bishops(board, white_to_move):

    # position vom schwarzen und weißen läufer finden
    #
    board = board.board

    score_to_return = 0

    if white_to_move:
        piece = 3
        pawn_piece = -1
    else :
        piece = -3
        pawn_piece =1
    
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
    
    
    if black_square_bishop == 1 and pawn_piece_count_black_square >= 2 :
        score_to_return += 20
    elif white_sqare_bishop == 1 and pawn_piece_count_white_square >= 2 :
        score_to_return += 20
    else:
        pass

    if white_to_move:
        return -score_to_return
    else:
        return  score_to_return



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

# bestrafung für einen läufer in anfangsposition 
def punish_bishop_on_SP(board, white_to_move):
    game_board = board.board
    score = 0
    if white_to_move:
        if game_board[7][2] == 3 :
            score -=15
        if game_board[7][5] == 3:
            score -= 15
        return score
        
    else:
        if game_board[0][2] == -3 :
            score +=15
            
        if game_board[0][5] == -3:
            score += 15
    
        return score
    

#Bonus, wenn beide Läufer vorhanden sind [20]

def bonus_both_bishops(board,  white_to_move):
    count = 0

    if white_to_move:
        piece = 3
    else:
        piece = -3
    
    game_board = board.board
    for x in range(len(game_board)):
        for i in range(len(game_board[x])):
            if game_board[x][i] == piece:
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

    game_board = board.board
    score = 0
    for row in range_test:
        for col in range(len(game_board[row])):
            a = game_board[row][col]
            if a == 0 : pass
            else:
                if col == 0 :
                    
                    if game_board[row][col] == piece and game_board[row + alpha][col+1] == piece:
                        pass
                    else:
                        score += 15
                
                elif col == 7:

                    if game_board[row][col] == piece and game_board[row + alpha][col-1] == piece:
                        pass
                    else:
                        score += 15

                else:

                    if game_board[row][col] == piece and (game_board[row + alpha][col-1] == piece or game_board[row + alpha][col+1] == piece):
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
    
    game_board = board.board
    count = 0
    for col in range(len(game_board[row])):
        if game_board[row][col] == piece and game_board[row+alpha][col] == 0 :
            count += 1
    
    if white_to_move:
        return (300 *count)
    else:
        return -(300 *count)


#Bestrafung, wenn die Möglichkeit einer Rochade vergeben wurde [20]


            




# bonus für einen bauern, der das Zentrum des schachbretts erreicht hat
def bonus_pawns_in_centre(board, white_to_move):
# slice the centre of the map , die mittleren 16 felder

    game_board = board.board
    centre = [game_board[x][2:6] for x in range(2,6)]
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
    
    new_board = np.array(board.board)
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
    
    new_board = np.array(board.board)
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
    new_board = np.array(board.board)
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

    new_board = np.array(board.board)
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
    score += bonus_pawns_in_centre(board, white_to_move)
    score += punish_for_pawns_not_right_aligned(board, white_to_move)
    score += bonus_paws_neighbor_lines(board, white_to_move)
    score += punish_isolated_pawns(board, white_to_move)
    score += punish_backward_pawns(board, white_to_move)
    return score


    return score

def evaluate_bishop_features(board, white_to_move):

    score = 0
    score += punish_bishop_on_SP(board, white_to_move)
    score += bonus_both_bishops(board, white_to_move)
    score += bishop_mobility(board, white_to_move)
    score += trapped_bishops(board,white_to_move)

    return score

def evaluate_rook_features(board, white_to_move):
    
    score = 0
    score += bonus_Rook_covered_rook(board, white_to_move)
    score += bonus_for_Rook_halfopen_lines(board , white_to_move)
    score += bonus_for_Rook_open_lines(board, white_to_move)
    score += rook_moobility(board, white_to_move)
    score += rooks_on_seventh_rank(board, white_to_move)

    return score

def evaluate_king_features(board, white_to_move):
    score = 0
    score += evaluate_king_danger(board, white_to_move)
    score += evaluate_king_shelter(board, white_to_move)
    return score


        
        

def eval_func(board, white_to_move, move=None):
    
    score_to_return = 0
    score_to_return += evaluate_pawn_features(board, white_to_move)
    score_to_return += evaluate_rook_features(board, white_to_move)
    score_to_return += evaluate_bishop_features(board, white_to_move)
    score_to_return += evaluate_king_features(board, white_to_move)
    score_to_return += material_evaluation(board, white_to_move)
    score_to_return += queen_on_seventh_rank(board, white_to_move)
    score_to_return += add_randomness()

    return score_to_return
