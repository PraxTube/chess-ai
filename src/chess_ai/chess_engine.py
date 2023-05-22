import numpy as np


class Board:
    def __init__(self, fen_board=None):
        if not fen_board:
            self.setup_default_board()
        else:
            self.setup_fen_board(fen_board)

    def __str__(self):
        result = ""
        for rank in self.board:
            current_rank = ""
            for square in rank:
                if square == "--":
                    current_rank += ". "
                else:
                    current_rank += (
                        square[1].upper() if square[0] == "w" else square[1].lower()
                    )
                    current_rank += " "
            result += current_rank.rstrip() + "\n"
        return result.rstrip()

    def fen(self):
        fen = ""
        for row in self.board:
            empty_count = 0
            for square in row:
                if square == "--":
                    empty_count += 1
                    continue

                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0

                if square[0] == "w":
                    fen += square[1].upper()
                else:
                    fen += square[1].lower()
            if empty_count > 0:
                fen += str(empty_count)
            fen += "/"
        # Remove the trailing '/'
        fen = fen[:-1]

        # Add the active color
        fen += " {} ".format("w" if self.white_to_move else "b")
        # Add the castling availability
        if self.current_castling_rights.any():
            sides = np.array(["K", "Q", "k", "q"])
            fen += "".join(sides[self.current_castling_rights]) + " "
        else:
            fen += "- "
        # Add the en passant target square
        fen += "- "
        # Add the half-move and full-move counters
        fen += "0 1"

        return fen

    def fen_to_board(self, fen):
        board = [["--"] * 8 for _ in range(8)]
        fen_board = fen.split(" ")[0]

        rank_strs = fen_board.split("/")
        for i, rank_str in enumerate(rank_strs):
            file_idx = 0
            for char in rank_str:
                if char.isdigit():
                    file_idx += int(char)
                else:
                    board[i][file_idx] = char
                    file_idx += 1

        for rank in board:
            for i, square in enumerate(rank):
                if square == "--":
                    continue

                if square.islower():
                    c = "p" if square == "p" else square.upper()
                    rank[i] = "b" + c
                else:
                    c = "p" if square == "P" else square.upper()
                    rank[i] = "w" + c
        return board

    def to_np(self):
        piece_values = {
            "--": 0,  # Empty square
            "wp": 1,  # White Pawn
            "wN": 2,  # White Knight
            "wB": 3,  # White Bishop
            "wR": 4,  # White Rook
            "wQ": 5,  # White Queen
            "wK": 6,  # White King
            "bp": -1,  # Black Pawn
            "bN": -2,  # Black Knight
            "bB": -3,  # Black Bishop
            "bR": -4,  # Black Rook
            "bQ": -5,  # Black Queen
            "bK": -6,  # Black King
        }

        board_as_np = np.array(
            [[piece_values[piece] for piece in row] for row in self.board]
        )
        return board_as_np

    def setup_default_board(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.moveFunctions = {
            "p": self.pawn_moves,
            "R": self.rook_moves,
            "N": self.knight_moves,
            "B": self.bishop_moves,
            "Q": self.queen_moves,
            "K": self.king_moves,
        }
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.pins = []
        self.checks = []
        self.enpassant_possible = ()
        self.enpassant_possible_log = [self.enpassant_possible]
        self.current_castling_rights = np.array([True, True, True, True])
        self.castle_rights_log = [self.current_castling_rights.copy()]

    def setup_fen_board(self, fen_board):
        self.board = self.fen_to_board(fen_board)
        self.moveFunctions = {
            "p": self.pawn_moves,
            "R": self.rook_moves,
            "N": self.knight_moves,
            "B": self.bishop_moves,
            "Q": self.queen_moves,
            "K": self.king_moves,
        }
        self.white_to_move = fen_board.split()[1] == "w"
        self.white_king_location = self.find_piece("wK")
        self.black_king_location = self.find_piece("bK")
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        fen_castle_rights = fen_board.split()[2]
        self.pins = []
        self.checks = []
        self.move_log = []
        self.enpassant_possible = ()
        self.enpassant_possible_log = [self.enpassant_possible]
        self.current_castling_rights = np.array(
            [
                "K" in fen_castle_rights,
                "Q" in fen_castle_rights,
                "k" in fen_castle_rights,
                "q" in fen_castle_rights,
            ]
        )
        self.castle_rights_log = [self.current_castling_rights.copy()]

    def find_piece(self, piece):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == piece:
                    return (row, col)
        raise ValueError("The given piece is no longer on the board", self.board, piece)

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log the move so we can undo it later
        self.white_to_move = not self.white_to_move  # switch players
        # update king's location if moved
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"

        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = "--"  # capturing the pawn

        # update enpassant_possible variable
        if (
            move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2
        ):  # only on 2 square pawn advance
            self.enpassant_possible = (
                (move.start_row + move.end_row) // 2,
                move.start_col,
            )
        else:
            self.enpassant_possible = ()

        # castle move
        if move.is_castle_move:
            if move.end_col - move.start_col == 2:  # king-side castle move
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][
                    move.end_col + 1
                ]  # moves the rook to its new square
                self.board[move.end_row][move.end_col + 1] = "--"  # erase old rook
            else:  # queen-side castle move
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][
                    move.end_col - 2
                ]  # moves the rook to its new square
                self.board[move.end_row][move.end_col - 2] = "--"  # erase old rook

        self.enpassant_possible_log.append(self.enpassant_possible)

        self.update_castle_rights(move)
        self.castle_rights_log.append(self.current_castling_rights.copy())

    def undo_move(self):
        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move  # swap players
            # update the king's position if needed
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)
            # undo en passant move
            if move.is_enpassant_move:
                self.board[move.end_row][
                    move.end_col
                ] = "--"  # leave landing square blank
                self.board[move.start_row][move.end_col] = move.piece_captured

            self.enpassant_possible_log.pop()
            self.enpassant_possible = self.enpassant_possible_log[-1]

            # undo castle rights
            self.castle_rights_log.pop()
            self.current_castling_rights = self.castle_rights_log[-1].copy()
            # undo the castle move
            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # king-side
                    self.board[move.end_row][move.end_col + 1] = self.board[
                        move.end_row
                    ][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = "--"
                else:  # queen-side
                    self.board[move.end_row][move.end_col - 2] = self.board[
                        move.end_row
                    ][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = "--"
            self.checkmate = False
            self.stalemate = False

    def update_castle_rights(self, move):
        if move.piece_captured == "wR":
            if move.end_col == 0:  # left rook
                self.current_castling_rights[1] = False
            elif move.end_col == 7:  # right rook
                self.current_castling_rights[0] = False
        elif move.piece_captured == "bR":
            if move.end_col == 0:  # left rook
                self.current_castling_rights[3] = False
            elif move.end_col == 7:  # right rook
                self.current_castling_rights[2] = False

        if move.piece_moved == "wK":
            self.current_castling_rights[1] = False
            self.current_castling_rights[0] = False
        elif move.piece_moved == "bK":
            self.current_castling_rights[3] = False
            self.current_castling_rights[2] = False
        elif move.piece_moved == "wR":
            if move.start_row == 7:
                if move.start_col == 0:  # left rook
                    self.current_castling_rights[1] = False
                elif move.start_col == 7:  # right rook
                    self.current_castling_rights[0] = False
        elif move.piece_moved == "bR":
            if move.start_row == 0:
                if move.start_col == 0:  # left rook
                    self.current_castling_rights[3] = False
                elif move.start_col == 7:  # right rook
                    self.current_castling_rights[2] = False

    def legal_moves(self):
        temp_castle_rights = self.current_castling_rights.copy()
        moves = []
        self.in_check, self.pins, self.checks = self.pins_and_checks()

        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:  # only 1 check, block the check or move the king
                moves = self.pseudo_legal_moves()
                # to block the check you must put a piece into one of the squares
                # between the enemy piece and your king
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []
                # if knight, must capture the knight or move your king,
                # other pieces can be blocked
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (
                            king_row + check[2] * i,
                            king_col + check[3] * i,
                        )  # check[2] and check[3] are the check directions
                        valid_squares.append(valid_square)
                        if (
                            valid_square[0] == check_row
                            and valid_square[1] == check_col
                        ):  # once you get to piece and check
                            break
                # get rid of any moves that don't block check or move king
                for i in range(
                    len(moves) - 1, -1, -1
                ):  # iterate through the list backwards when removing elements
                    if (
                        moves[i].piece_moved[1] != "K"
                    ):  # move doesn't move king so it must block or capture
                        if (
                            not (moves[i].end_row, moves[i].end_col) in valid_squares
                        ):  # move doesn't block or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.king_moves(king_row, king_col, moves)
        else:  # not in check - all moves are fine
            moves = self.pseudo_legal_moves()
            if self.white_to_move:
                self.castle_moves(
                    self.white_king_location[0], self.white_king_location[1], moves
                )
            else:
                self.castle_moves(
                    self.black_king_location[0], self.black_king_location[1], moves
                )

        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.current_castling_rights = temp_castle_rights
        return moves

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(
                self.white_king_location[0], self.white_king_location[1]
            )
        else:
            return self.square_under_attack(
                self.black_king_location[0], self.black_king_location[1]
            )

    def square_under_attack(self, row, col):
        self.white_to_move = not self.white_to_move
        opponents_moves = self.pseudo_legal_moves()
        self.white_to_move = not self.white_to_move
        for move in opponents_moves:
            if move.end_row == row and move.end_col == col:  # square is under attack
                return True
        return False

    def pseudo_legal_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if not (
                    (turn == "w" and self.white_to_move)
                    or (turn == "b" and not self.white_to_move)
                ):
                    continue

                piece = self.board[row][col][1]
                self.moveFunctions[piece](row, col, moves)
        return moves

    def pins_and_checks(self):
        pins = []  # squares pinned and the direction its pinned from
        checks = []  # squares where enemy is applying a check
        in_check = False
        if self.white_to_move:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]

        # check outwards from king for pins and checks, keep track of pins
        directions = (
            (-1, 0),
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        )
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()  # reset possible pins
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if not (0 <= end_row <= 7 and 0 <= end_col <= 7):
                    break

                end_piece = self.board[end_row][end_col]
                if end_piece[0] == ally_color and end_piece[1] != "K":
                    if possible_pin != ():
                        break

                    possible_pin = (
                        end_row,
                        end_col,
                        direction[0],
                        direction[1],
                    )
                elif end_piece[0] == enemy_color:
                    enemy_type = end_piece[1]
                    # 5 possibilities in this complex conditional
                    # 1.) orthogonally away from king and piece is a rook
                    # 2.) diagonally away from king and piece is a bishop
                    # 3.) 1 square away diagonally from king and piece is a pawn
                    # 4.) any direction and piece is a queen
                    # 5.) any direction 1 square away and piece is a king
                    if not (
                        (0 <= j <= 3 and enemy_type == "R")
                        or (4 <= j <= 7 and enemy_type == "B")
                        or (
                            i == 1
                            and enemy_type == "p"
                            and (
                                (enemy_color == "w" and 6 <= j <= 7)
                                or (enemy_color == "b" and 4 <= j <= 5)
                            )
                        )
                        or (enemy_type == "Q")
                        or (i == 1 and enemy_type == "K")
                    ):
                        break

                    if possible_pin == ():  # no piece blocking, so check
                        in_check = True
                        checks.append((end_row, end_col, direction[0], direction[1]))
                        break
                    else:  # piece blocking so pin
                        pins.append(possible_pin)
                        break
        # check for knight checks
        knight_moves = (
            (-2, -1),
            (-2, 1),
            (-1, 2),
            (1, 2),
            (2, -1),
            (2, 1),
            (-1, -2),
            (1, -2),
        )
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if not (0 <= end_row <= 7 and 0 <= end_col <= 7):
                continue

            end_piece = self.board[end_row][end_col]
            if not (end_piece[0] == enemy_color and end_piece[1] == "N"):
                continue

            in_check = True
            checks.append((end_row, end_col, move[0], move[1]))
        return in_check, pins, checks

    def pawn_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            move_amount = -1
            start_row = 6
            enemy_color = "b"
            king_row, king_col = self.white_king_location
        else:
            move_amount = 1
            start_row = 1
            enemy_color = "w"
            king_row, king_col = self.black_king_location

        if self.board[row + move_amount][col] == "--":  # 1 square pawn advance
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((row, col), (row + move_amount, col), self.board))
                if (
                    row == start_row and self.board[row + 2 * move_amount][col] == "--"
                ):  # 2 square pawn advance
                    moves.append(
                        Move((row, col), (row + 2 * move_amount, col), self.board)
                    )
        if col - 1 >= 0:  # capture to the left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[row + move_amount][col - 1][0] == enemy_color:
                    moves.append(
                        Move((row, col), (row + move_amount, col - 1), self.board)
                    )
                if (row + move_amount, col - 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(king_col + 1, col - 1)
                            outside_range = range(col + 1, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, col, -1)
                            outside_range = range(col - 2, -1, -1)
                        for i in inside_range:
                            if (
                                self.board[row][i] != "--"
                            ):  # some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (
                                square[1] == "R" or square[1] == "Q"
                            ):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(
                            Move(
                                (row, col),
                                (row + move_amount, col - 1),
                                self.board,
                                is_enpassant_move=True,
                            )
                        )
        if col + 1 <= 7:  # capture to the right
            if not piece_pinned or pin_direction == (move_amount, +1):
                if self.board[row + move_amount][col + 1][0] == enemy_color:
                    moves.append(
                        Move((row, col), (row + move_amount, col + 1), self.board)
                    )
                if (row + move_amount, col + 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(king_col + 1, col)
                            outside_range = range(col + 2, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, col + 1, -1)
                            outside_range = range(col - 1, -1, -1)
                        for i in inside_range:
                            if (
                                self.board[row][i] != "--"
                            ):  # some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[row][i]
                            if square[0] == enemy_color and (
                                square[1] == "R" or square[1] == "Q"
                            ):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(
                            Move(
                                (row, col),
                                (row + move_amount, col + 1),
                                self.board,
                                is_enpassant_move=True,
                            )
                        )

    def rook_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                # can't remove queen from pin on rook moves,
                # only remove it on bishop moves
                if self.board[row][col][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if not (0 <= end_row <= 7 and 0 <= end_col <= 7):
                    break

                if not (
                    not piece_pinned
                    or pin_direction == direction
                    or pin_direction == (-direction[0], -direction[1])
                ):
                    break

                end_piece = self.board[end_row][end_col]
                if end_piece == "--":
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                elif end_piece[0] == enemy_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                    break
                else:
                    break

    def knight_moves(self, row, col, moves):
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                self.pins.remove(self.pins[i])
                return

        knight_moves = (
            (-2, -1),
            (-2, 1),
            (-1, 2),
            (1, 2),
            (2, -1),
            (2, 1),
            (-1, -2),
            (1, -2),
        )  # up/left up/right right/up right/down down/left down/right left/up left/down
        ally_color = "w" if self.white_to_move else "b"
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if not (0 <= end_row <= 7 and 0 <= end_col <= 7):
                continue

            end_piece = self.board[end_row][end_col]
            if end_piece[0] != ally_color:
                moves.append(Move((row, col), (end_row, end_col), self.board))

    def bishop_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = (
            (-1, -1),
            (-1, 1),
            (1, 1),
            (1, -1),
        )  # diagonals: up/left up/right down/right down/left
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if not (0 <= end_row <= 7 and 0 <= end_col <= 7):
                    break

                if not (
                    not piece_pinned
                    or pin_direction == direction
                    or pin_direction == (-direction[0], -direction[1])
                ):
                    continue

                end_piece = self.board[end_row][end_col]
                if end_piece == "--":
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                elif end_piece[0] == enemy_color:  # capture enemy piece
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                    break
                else:
                    break

    def queen_moves(self, row, col, moves):
        self.bishop_moves(row, col, moves)
        self.rook_moves(row, col, moves)

    def king_moves(self, row, col, moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.white_to_move else "b"

        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]
            if not (0 <= end_row <= 7 and 0 <= end_col <= 7):
                continue

            end_piece = self.board[end_row][end_col]
            if end_piece[0] == ally_color:
                continue

            # place king on end square and check for checks
            if ally_color == "w":
                self.white_king_location = (end_row, end_col)
            else:
                self.black_king_location = (end_row, end_col)

            in_check, pins, checks = self.pins_and_checks()
            if not in_check:
                moves.append(Move((row, col), (end_row, end_col), self.board))

            # place king back on original location
            if ally_color == "w":
                self.white_king_location = (row, col)
            else:
                self.black_king_location = (row, col)

    def castle_moves(self, row, col, moves):
        if self.square_under_attack(row, col):
            return  # can't castle while in check

        if (self.white_to_move and self.current_castling_rights[0]) or (
            not self.white_to_move and self.current_castling_rights[2]
        ):
            self.kingside_castle_moves(row, col, moves)
        if (self.white_to_move and self.current_castling_rights[1]) or (
            not self.white_to_move and self.current_castling_rights[3]
        ):
            self.queenside_castle_moves(row, col, moves)

    def kingside_castle_moves(self, row, col, moves):
        if not (self.board[row][col + 1] == "--" and self.board[row][col + 2] == "--"):
            return

        if not (
            self.square_under_attack(row, col + 1)
            and not self.square_under_attack(row, col + 2)
        ):
            moves.append(
                Move((row, col), (row, col + 2), self.board, is_castle_move=True)
            )

    def queenside_castle_moves(self, row, col, moves):
        if not (
            self.board[row][col - 1] == "--"
            and self.board[row][col - 2] == "--"
            and self.board[row][col - 3] == "--"
        ):
            return

        if not (
            self.square_under_attack(row, col - 1)
            and not self.square_under_attack(row, col - 2)
        ):
            moves.append(
                Move((row, col), (row, col - 2), self.board, is_castle_move=True)
            )


class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(
        self,
        start_square,
        end_square,
        board,
        is_enpassant_move=False,
        is_castle_move=False,
    ):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # pawn promotion
        self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_row == 0) or (
            self.piece_moved == "bp" and self.end_row == 7
        )
        # en passant
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"
        # castle move
        self.is_castle_move = is_castle_move

        self.is_capture = self.piece_captured != "--"
        self.moveID = (
            self.start_row * 1000
            + self.start_col * 100
            + self.end_row * 10
            + self.end_col
        )

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def chess_notation(self):
        if self.is_pawn_promotion:
            return self.rank_file(self.end_row, self.end_col) + "Q"
        if self.is_castle_move:
            if self.end_col == 1:
                return "0-0-0"
            else:
                return "0-0"
        if self.is_enpassant_move:
            return (
                self.rank_file(self.start_row, self.start_col)[0]
                + "x"
                + self.rank_file(self.end_row, self.end_col)
                + " e.p."
            )
        if self.piece_captured != "--":
            if self.piece_moved[1] == "p":
                return (
                    self.rank_file(self.start_row, self.start_col)[0]
                    + "x"
                    + self.rank_file(self.end_row, self.end_col)
                )
            else:
                return (
                    self.piece_moved[1]
                    + "x"
                    + self.rank_file(self.end_row, self.end_col)
                )
        else:
            if self.piece_moved[1] == "p":
                return self.rank_file(self.end_row, self.end_col)
            else:
                return self.piece_moved[1] + self.rank_file(self.end_row, self.end_col)

        # TODO Disambiguating moves

    def rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def coordinate(self):
        """
        Returns coordinate notation
        """
        if self.is_castle_move:
            return "0-0" if self.end_col == 6 else "0-0-0"

        start_square = self.rank_file(self.start_row, self.start_col)
        end_square = self.rank_file(self.end_row, self.end_col)

        if self.is_pawn_promotion:
            return start_square + end_square + "q"

        return start_square + end_square

    def __str__(self):
        """
        Returns algebraic notation
        """
        if self.is_castle_move:
            return "0-0" if self.end_col == 6 else "0-0-0"

        end_square = self.rank_file(self.end_row, self.end_col)

        if self.piece_moved[1] == "p":
            if self.is_capture:
                return self.cols_to_files[self.start_col] + "x" + end_square
            else:
                return end_square + "Q" if self.is_pawn_promotion else end_square

        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square
