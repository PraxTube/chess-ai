import chess_ai.test2 as test
import chess_ai.chess_engine as chess



def test_punish_bishop_on_SP():

    board = chess.Board()

    # test für weiß starting position
    assert(test.punish_bishop_on_SP(board.board, True) == -30)
    # test für schwarz starting position
    assert(test.punish_bishop_on_SP(board.board, False) == 30)

    board = chess.Board(fen_board=  "rn1qkbnr/pp2pppp/2p5/3p4/3P1Bb1/2P1P3/PP3PPP/RN1QKBNR b KQkq - 0 1")
    # ein läufer sit herausgezogen von der starting position
    assert(test.punish_bishop_on_SP(board.board, True) == -15)
    # ein läufer sit herausgezogen von der starting position
    assert(test.punish_bishop_on_SP(board.board, False)== 15)

def test_bonus_both_bishops():
    # im fen-string nur ein schwarzer bishop / 2 weiße bishops
    board = chess.Board(fen_board="rn1qkbnr/pp2pp1p/2p3p1/3p4/3P1BP1/2P1P3/PP3PP1/RN1QKBNR b KQkq - 0 1") 
    assert(test.bonus_both_bishops(board.board, False) == 0)
    
    assert(test.bonus_both_bishops(board.board, True) == 20)

    # auf beiden seiten nur noch ein läufer vorhanden

    board = chess.Board(fen_board="rn1qkbnr/pp3p1p/2p3p1/3p4/P2P1pP1/2P1P3/1P3PP1/RN1QKBNR w KQkq - 0 1")

    assert(test.bonus_both_bishops(board.board, True) == 0)
    assert(test.bonus_both_bishops(board.board, False) == 0)


def test_punish_for_pawns_not_right_aligned():
    # die baunern stehen in einem komischen zick zack 4 bauern von schwarz und 4 bauner bon weiß decken jeweils keinen andere bauer
    board = chess.Board(fen_board="bbnrnkrq/p1p1p1p1/1p1p1p1p/8/8/1P1P1P1P/P1P1P1P1/BBNRNKRQ w - - 0 1")

    assert(test.punish_for_pawns_not_right_aligned(board.board, True) == -60)
    assert(test.punish_for_pawns_not_right_aligned(board.board, False) == 60)

    # die bauern stehen in einer bauern kette, trotzdem decken 3 bauern jeweils keine anderen

    board = chess.Board(fen_board="nrbkrbnq/pp3p1p/2p1p1p1/3p4/3P4/2P1P1P1/PP3P1P/NRBKRBNQ w - - 0 1")

    assert(test.punish_for_pawns_not_right_aligned(board.board, True) == -30)
    assert(test.punish_for_pawns_not_right_aligned(board.board, False) == 30)

def test_pawn_promotion_poss():
    # ein weißer bauer ist in er vorletzten reihe
    board = chess.Board(fen_board="nqr1krbb/pppP3p/3Pnpp1/1P6/5P2/8/P1P1pKPP/NQRN1RBB b - - 0 1")

    assert(test.pawn_promotion_poss(board.board, True) == 300)

    assert(test.pawn_promotion_poss(board.board, False) == -300)
    
    # weißer bauer auf der vorletzten
    board = chess.Board(fen_board="nqr1krbb/p1p1pppp/1p1Pn3/8/3P4/8/PP2PPPP/NQRNKRBB b - - 0 1")

    assert(test.pawn_promotion_poss(board.board, True)== 0)
    assert(test.pawn_promotion_poss(board.board, False)== 0)

    board = chess.Board(fen_board="rnbqkbnr/p3pppp/8/1p4B1/6P1/N2P4/Ppp1PP1P/R2QKBNR b KQkq - 0 1")

    assert(test.pawn_promotion_poss(board.board, False)== -600)
    assert(test.pawn_promotion_poss(board.board, True) == 0)

def test_bonus_pawns_in_centre():
    board = chess.Board(fen_board="brnqknrb/pp4pp/5p2/2ppp3/3PP3/2P2P2/PP4PP/RBNQKNBR w - - 0 1")

    assert(test.bonus_pawns_in_centre(board.board, True) == 60)
    assert(test.bonus_pawns_in_centre(board.board, False) == -60)
    
    board = chess.Board(fen_board="brnqknrb/ppp3pp/5p2/3pp3/4P3/2P5/PP1P1PPP/RBNQKNBR w - - 0 1")

    assert(test.bonus_pawns_in_centre(board.board, True) == 30)
    assert(test.bonus_pawns_in_centre(board.board, False) == -45)

def  test_punish_pawns_same_line():

    board = chess.Board(fen_board="brnqknrb/2p2ppp/4p3/pP1P4/1P1P4/8/2P2PPP/RBNQKNBR b - - 0 1")

    assert(test.punish_pawns_same_line(board.board, True) == -60)

    assert(test.punish_pawns_same_line(board.board, False) == 0)

    board = chess.Board(fen_board="brnqknrb/pppp4/8/4p2p/4pp2/6P1/PPPP3P/RBNQKNBR w - - 0 1")

    assert(test.punish_pawns_same_line(board.board, True) == 0)
    assert(test.punish_pawns_same_line(board.board, False) == 30)

def test_bonus_paws_neighbor_lines():
    board = chess.Board(fen_board="brnqknrb/8/8/7p/P4p2/2P5/8/RBNQKNBR b - - 0 1")

    assert(test.bonus_paws_neighbor_lines(board.board, True) == 40 )
    assert(test.bonus_paws_neighbor_lines(board.board, False) == -40 )


def test_bonus_for_Rook_halfopen_lines():

    board = chess.Board(fen_board="brnqknrb/8/8/7p/P4p2/2P5/8/RBNQKNBR b - - 0 1")

    assert(test.bonus_for_Rook_halfopen_lines(board.board, True) == 30)
    assert(test.bonus_for_Rook_halfopen_lines(board.board, False) == 0)

    board = chess.Board(fen_board="brnqknrb/8/8/8/1P3pP1/2P5/8/1BNQKNBR b - - 0 1")

    assert(test.bonus_for_Rook_halfopen_lines(board.board, True) == 0)


def test_bonus_for_Rook_open_lines():
    
    board = chess.Board(fen_board="brnqknrb/8/8/8/1P3pP1/2P5/8/1BNQKNBR b - - 0 1")

    assert(test.bonus_for_Rook_open_lines(board.board, True) == 15)
    assert(test.bonus_for_Rook_open_lines(board.board, False) == 0)

def test_bonus_Rook_covered_rook():
    board = chess.Board(fen_board="brnqknrb/8/8/8/1P3pP1/2P5/R6R/1BNQKNB1 b - - 0 1")

    assert(test.bonus_Rook_covered_rook(board, True) == 30)