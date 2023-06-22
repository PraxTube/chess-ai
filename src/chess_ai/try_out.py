import  chess_engine as chess

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


board = chess.Board(fen_board="nrbkrbnq/pp3p1p/2p1p1p1/3p4/3P4/2P1P1P1/PP3P1P/NRBKRBNQ w - - 0 1")

x = punish_for_pawns_not_right_aligned(board.board, True)

print(x)