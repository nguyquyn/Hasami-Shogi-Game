# Author: Quynh Nguyen
# Date: December 3rd, 2021
# Description: Write a program for the game Hasami Shogi. Add the required methods as assigned but also can add other classes, methods, or data members.


class HasamiShogiGame:
    """
    Class to represent Hasami Shogi game, played by 2 players (red or black). The first player will start with black pieces then players will alternate turns.
    Pawns can only move horizontally or vertically and are captured if the opposite color are on adjacent sides.
    Pieces can also be captured if the piece is orthogonally surrounded by the opposing color pieces (ex. in a corner).
    Captures can be made on multiple sides (up to 3 sides).
    The winner is decided when all pieces are captured but 1 or no pieces are left.
    """

    def __init__(self):
        """
        Constructor for HasamiShogiGame class that takes no parameters. Initializes data members.
        Set game state to "UNFINISHED".
        Set current turn to black player to start.
        Set all captured pieces to 0.
        All data members are private.
        """
        self._board = []
        self._board.append(Piece("RED", "a1"))
        self._board.append(Piece("RED", "a2"))
        self._board.append(Piece("RED", "a3"))
        self._board.append(Piece("RED", "a4"))
        self._board.append(Piece("RED", "a5"))
        self._board.append(Piece("RED", "a6"))
        self._board.append(Piece("RED", "a7"))
        self._board.append(Piece("RED", "a8"))
        self._board.append(Piece("RED", "a9"))
        self._board.append(Piece("BLACK", "i1"))
        self._board.append(Piece("BLACK", "i2"))
        self._board.append(Piece("BLACK", "i3"))
        self._board.append(Piece("BLACK", "i4"))
        self._board.append(Piece("BLACK", "i5"))
        self._board.append(Piece("BLACK", "i6"))
        self._board.append(Piece("BLACK", "i7"))
        self._board.append(Piece("BLACK", "i8"))
        self._board.append(Piece("BLACK", "i9"))

        self._current_game_state = "UNFINISHED"
        self._current_player_turn = "BLACK"
        self._red_pieces_captured = 0
        self._black_pieces_captured = 0

    def get_game_state(self):
        """
        Method that takes no parameters and checks if the game is still being played or a winner (black or red) have been decided.
        :return:
            "UNFINISHED": if the game is still being played
            "RED_WON": if red player won
            "BLACK_WON": if black player won
        """
        return self._current_game_state

    def get_active_player(self):
        """
        Method that takes no parameters and checks whose turn is it.
        :return:
            "RED": if it is the red player's turn
            "BLACK": if it is the black player's turn
        """
        return self._current_player_turn

    def get_num_captured_pieces(self, player_color):
        """
        Method that takes 1 parameter to get number of how many captured pieces of red or black.
        :param player_color: represents black player or red player
        :return: # of pieces of the color that has been captured
        """
        if player_color == "RED":
            return self._black_pieces_captured
        return self._red_pieces_captured

    def get_square_occupant(self, square_occupied):
        """
        Method that takes 1 parameter and checks if the square is currently being occupied by a red or black piece, or is empty.
        :param square_occupied: string that represents a square (ex. "i7")
        :return:
            "RED": square is occupied by a red piece
            "BLACK": square is occupied by a black piece
            "NONE": square is not occupied by any pieces
        """
        for piece in self._board:
            if piece.get_square() == square_occupied:
                return piece.get_color()
        return "RED"

    def switch_player_turn(self, player_color):
        """
        Method that takes 1 parameter to switch between red or black player's turn. Checks if the player made a valid move and then updates the turn to the other player.
        :param player_color: represents black player or red player's turn
        """
        if self._current_player_turn == player_color:
            return "ALREADY SET"
        else:  # next player
            self._current_player_turn = player_color

    def make_move(self, square_moved_from, square_moved_to):
        """
        Method that takes 2 parameters and make indicated move, remove any captured pieces, and update the game state and player's turn.
        :param square_moved_from: string that represents square that piece is moving from
        :param square_moved_to: string that represents square that piece will be moving to
        :return:
            False: if piece being moved from is not the same color as the player's turn OR if the move is not legal OR if the game has already been won
            True: if piece is being moved from is the same color as the player's turn AND if the move is legal AND if the game is still playing and has not finished
        """

        color_from = self.get_square_occupant(square_moved_from)
        # if colored piece is not moved by corresponding player
        if color_from != self.get_active_player():
            return False
        if color_from == "NONE":
            return False
        color_to = self.get_square_occupant(square_moved_to)
        if color_to != "NONE":
            return False

        # if game has already been won
        if self.get_game_state() != "UNFINISHED":
            return False

        # if unable to move horizontally/vertically due to blocked piece
        if self.num_of_ways_to_move(square_moved_from, square_moved_to) is False:
            return False

        # move pieces
        self.change_quadrant(square_moved_to, square_moved_from)

        # see if pieces can be captured, remove any captured pieces
        self.check_capture(square_moved_to)

        # if game is not finished, continue playing
        if self.get_game_state() != "UNFINISHED":
            return False

        # update whose turn it is
        if self.get_active_player() == "BLACK":
            self.switch_player_turn("RED")
        else:
            self.switch_player_turn("BLACK")

        return True

    def change_quadrant(self, square_moved_from, square_moved_to):
        """
        Method that takes 2 parameters and move piece from 1 square to another given piece can be moved vertically/horizontally.
        :param square_moved_from: string that represents square that piece is moving from
        :param square_moved_to: string that represents square that piece will be moving to
        """
        for piece in self._board:
            if piece.get_square() == square_moved_from:
                piece.set_square(square_moved_to)
                break

    def path_clear_test(self, list):
        """
        Method that takes 1 parameter to check if squares from beginning square to end square is clear
        :param list: list of different paths
        :return:
            False: if piece in path is occupied by piece
            True: if square in path is empty
        """
        list = []
        for x in list:
            if self.get_square_occupant(x) != "NONE":
                return False
        return True

    def num_of_ways_to_move(self, square_moved_from, square_moved_to):
        """
        Method that takes 2 parameters to see the number of different ways the piece can move to a square
        :param square_moved_from: string that represents square that piece is moving from
        :param square_moved_to: string that represents square that piece is moving to
        :return:
            False: if both paths have a piece that is occupying a square
        """
        # PATH 1 (go up/down first, go left/right second)
        # GO VERTICALLY
        path_1_pt_1 = []
        middle_point1 = square_moved_to[0] + square_moved_from[1]
        switch_to_beg_num1 = ord(square_moved_from[0])
        switch_to_middle1 = ord(middle_point1[0])

        # go up
        for index1 in range(switch_to_beg_num1, (switch_to_middle1 - 1), -1):
            all_num_up_down1 = chr(index1) + middle_point1[1]
            path_1_pt_1.append(all_num_up_down1)
        # go down
        for index1 in range(switch_to_beg_num1, (switch_to_middle1 + 1)):
            all_num_up_down1 = chr(index1) + middle_point1[1]
            path_1_pt_1.append(all_num_up_down1)

        # GO HORIZONTALLY
        path_1_pt_2 = []

        # go left
        for index2 in range(int(middle_point1[1]), (int(square_moved_to[1]) - 1), -1):
            all_num_left_right1 = square_moved_to[0] + str(index2)
            path_1_pt_2.append(all_num_left_right1)
        # go right
        for index2 in range(int(middle_point1[1]), int(square_moved_to[1]) + 1):
            all_num_left_right1 = square_moved_to[0] + str(index2)
            path_1_pt_2.append(all_num_left_right1)

        new_path1 = path_1_pt_1[1:] + path_1_pt_2[1:]

        # PATH 2 (go left/right first, go up/down second)
        # GO HORIZONTALLY
        path_2_pt_1 = []
        middle_point2 = square_moved_from[0] + square_moved_to[1]

        # go left
        for index3 in range(int(square_moved_from[1]), (int(middle_point2[1]) - 1), -1):
            all_num_left_right2 = square_moved_to[0] + str(index3)
            path_2_pt_1.append(all_num_left_right2)
        # go right
        for index3 in range(int(square_moved_from[1]), int(middle_point2[1]) + 1):
            all_num_left_right2 = square_moved_from[0] + str(index3)
            path_2_pt_1.append(all_num_left_right2)

        # GO VERTICALLY
        path_2_pt_2 = []
        switch_to_middle2 = ord(middle_point2[0])
        switch_to_end_num1 = ord(square_moved_to[0])

        # go up
        for index4 in range(switch_to_middle2, (switch_to_end_num1 - 1), -1):
            all_num_up_down2 = chr(index4) + middle_point2[1]
            path_2_pt_2.append(all_num_up_down2)
        # go down
        for index4 in range(switch_to_middle2, (switch_to_end_num1 + 1)):
            all_num_up_down2 = chr(index4) + middle_point2[1]
            path_2_pt_2.append(all_num_up_down2)

        new_path2 = path_2_pt_1[1:] + path_2_pt_2[1:]

        # check if there are pieces occupying a square in both paths
        if self.path_clear_test(new_path1) and self.path_clear_test(new_path2) is False:
            return False
        return True

    def check_capture(self, end_square):
        """
        Method that takes 1 parameter to see if piece in end_square is next to a piece of the same color, opposing piece, or next to square that is empty.
        :param end_square: piece that has been moved to square
        """
        temp_captured = []
        change_end_num = ord(end_square[0])
        top = ord("a")
        bottom = ord("i")
        current_player = self.get_active_player()

        # check pieces that are above end_square
        if change_end_num != top:
            for index5 in range(change_end_num, (top - 1), -1):
                new_num1 = chr(index5) + end_square[1]
                check1 = self.get_square_occupant(new_num1)
                if check1 == "NONE":
                    temp_captured = []
                    break
                elif check1 == current_player:
                    if len(temp_captured) > 0:
                        self.remove_captured_pieces(temp_captured)
                        if check1 == "RED":
                            self._black_pieces_captured += len(temp_captured)
                            if self._black_pieces_captured >= 8:
                                self._current_game_state = "RED WON"
                                return False
                            else:
                                self._current_game_state = "UNFINISHED"
                        elif check1 == "BLACK":
                            self._red_pieces_captured += len(temp_captured)
                            if self._red_pieces_captured >= 8:
                                self._current_game_state = "BLACK WON"
                                return False
                            else:
                                self._current_game_state = "UNFINISHED"
                        temp_captured = []
                else:
                    temp_captured.append(new_num1)

        # check pieces that are below end_square
        if change_end_num != bottom:
            for index6 in range(change_end_num, bottom, +1):
                new_num2 = chr(index6) + end_square[1]
                check2 = self.get_square_occupant(new_num2)
                if check2 == "NONE":
                    temp_captured = []
                    break
                elif check2 == current_player:
                    if len(temp_captured) > 0:
                        self.remove_captured_pieces(temp_captured)
                        if check2 == "RED":
                            self._black_pieces_captured += len(temp_captured)
                            if self._black_pieces_captured >= 8:
                                self._current_game_state = "RED WON"
                                return False
                            else:
                                self._current_game_state = "UNFINISHED"
                        elif check2 == "BLACK":
                            self._red_pieces_captured += len(temp_captured)
                            if self._red_pieces_captured >= 8:
                                self._current_game_state = "BLACK WON"
                                return False
                            else:
                                self._current_game_state = "UNFINISHED"
                        temp_captured = []
                else:
                    temp_captured.append(new_num2)

        # check pieces that are to the left of end_square
        if end_square[1] != "1":
            for index7 in range(int(end_square[1]), (int("1") - 1), -1):
                check3 = self.get_square_occupant(index7)
                if check3 == "NONE":
                    temp_captured = []
                    break
                elif check3 == current_player:
                    if len(temp_captured) > 0:
                        self.remove_captured_pieces(temp_captured)
                        if check3 == "RED":
                            self._black_pieces_captured += len(temp_captured)
                            if self._black_pieces_captured >= 8:
                                self._current_game_state = "RED WON"
                                return False
                            else:
                                self._current_game_state = "UNFINISHED"
                        elif check3 == "BLACK":
                            self._red_pieces_captured += len(temp_captured)
                            if self._red_pieces_captured >= 8:
                                self._current_game_state = "BLACK WON"
                                return False
                            else:
                                self._current_game_state = "UNFINISHED"
                        temp_captured = []
                else:
                    temp_captured.append(check3)

        # check pieces that are to the right of end_square
        if end_square[1] != "9":
            for index8 in range(int(end_square[1]), int("9"), +1):
                check4 = self.get_square_occupant(index8)
                if check4 == "NONE":
                    temp_captured = []
                    break
                elif check4 == current_player:
                    if len(temp_captured) > 0:
                        self.remove_captured_pieces(temp_captured)
                        if check4 == "RED":
                            self._black_pieces_captured += len(temp_captured)
                            if self._black_pieces_captured >= 8:
                                self._current_game_state = "RED WON"
                                return False
                            else:
                                self._current_game_state = "UNFINISHED"
                        elif check4 == "BLACK":
                            self._red_pieces_captured += len(temp_captured)
                            if self._red_pieces_captured >= 8:
                                self._current_game_state = "BLACK WON"
                                return False
                            else:
                                self._current_game_state = "UNFINISHED"
                        temp_captured = []
                else:
                    temp_captured.append(check4)

    def remove_captured_pieces(self, temp_captured):
        """
        Method that takes list of captured pieces and removes them from the board.
        :param temp_captured: list of captured pieces
        """
        for captured_pieces in temp_captured:
            self.remove_single_piece(captured_pieces)

    def remove_single_piece(self, piece):
        """
        Method that takes captured piece and removes it from the board.
        :param piece: captured piece
        """
        for single_piece in self._board:
            if single_piece.get_square() == piece:
                self._board.remove(single_piece)
                break


class Piece:
    """
    Class to represent a piece on the board. The piece is represented by the color red or black and if it is occupying a square.
    """

    def __init__(self, color, square):
        """
        Constructor for Piece class. Initializes data members.
        All data members are private.
        """
        self._color = color
        self._square = square

    def get_color(self):
        """
        Method that takes no parameters and gets the color of the piece.
        :return: color of piece
        """
        return self._color

    def get_square(self):
        """
        Method that takes no parameters and gets if the piece is on a square.
        :return: square that piece is located on square
        """
        return self._square

    def set_square(self, square):
        """
        Setter method to set square to be occupied by a piece.
        :param square: located on the board
        """
        self._square = square
