from images import *


class Piece:

    def __init__(self, color, piece_type, alive, placement):
        """
        initialize the piece
        :param color: color of piece ('w' or 'b')
        :param piece_type: type of piece ('p', 'r', 'b', 'kn', 'q' or 'k')
        :param alive: bool if pice if a live
        :param placement: place of piece on board (board index from 0-7 on each axis)
        """
        self.type = piece_type
        self.color = color
        self.alive = alive
        self.place = placement
        self.moved = False

    def kill(self):
        """
        kill a piece
        :return: None
        """
        self.alive = False

    def un_kill(self):
        """
        revive a pice
        :return: None
        """
        self.alive = True

    def change_place(self, placement):
        """
        change the place of a piece
        :param placement: new place of piece
        :return: None
        """
        self.place = placement


class Player:

    def __init__(self, color, ip=None, pieces=None, time_left=None):
        """
        initialize the player
        :param color: color of player ('b' or 'w')
        :param ip: ip address of player (optional)
        :param pieces: pieces of player (list of lists by piece-type)
        :param time_left: time left for player in a game
        """
        self.color = color
        self.ip = ip
        # time of player in seconds
        self.time_left = time_left
        if pieces is None:
            self.pieces = self.create_pieces()
        else:
            self.pieces = pieces

    def create_pieces(self):
        """
        create the pieces of a player
        :return: None
        """
        if self.color == 'w':
            y = 1
        else:
            y = 6

        pawns = []
        for i in range(8):
            pawns.append(Piece(self.color, 'p', True, (i, y)))

        if y == 1:
            y = 0
        else:
            y = 7

        # initialize the other pieces
        rooks = [Piece(self.color, 'r', True, (0, y)), Piece(self.color, 'r', True, (7, y))]
        knights = [Piece(self.color, 'kn', True, (1, y)), Piece(self.color, 'kn', True, (6, y))]
        bishops = [Piece(self.color, 'b', True, (2, y)), Piece(self.color, 'b', True, (5, y))]
        queens = [Piece(self.color, 'q', True, (3, y))]
        king = [Piece(self.color, 'k', True, (4, y))]

        return [king, pawns, bishops, rooks, queens, knights]


class Board:

    def __init__(self, white_player=None, black_player=None, orientation=None):
        """
        initialize a board
        :param white_player: the white player (Player object)
        :param black_player: the black player (Player object)
        :param orientation: orientation of board ('w' if white is down, 'b' if black is down)
        """
        self.white = white_player
        self.black = black_player
        self.turn = 'w'
        self.last_move = None
        self.orientation = orientation
        self.draw = None
        self.started = False
        self.game_time = None
        self.ended = False

    def change_turn(self):
        """
        toggle the turns
        :return: None
        """
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'

    def set_white(self, player):
        """
        set white player
        :param player: player to set
        :return:
        """
        self.white = player

    def set_black(self, player):
        """
        set black player
        :param player: player to set
        :return:
        """
        self.black = player

    def init_pieces(self):
        """
        initialize the pieces on the board
        :return: None
        """
        # initialize the pawns of both sides
        if self.orientation == 'w':
            y = 1
        else:
            y = 6

        white_pawns = []
        black_pawns = []
        for i in range(8):
            white_pawns.append(Piece('w', 'p', True, (i, y)))
            black_pawns.append(Piece('b', 'p', True, (i, 7 - y)))

        if self.orientation == 'w':
            y = 0
            x1 = 3
            x2 = 4
        else:
            y = 7
            x1 = 4
            x2 = 3

        # initialize the other pieces
        white_rooks = [Piece('w', 'r', True, (0, y)),
                       Piece('w', 'r', True, (7, y))]
        white_knights = [Piece('w', 'kn', True, (1, y)),
                         Piece('w', 'kn', True, (6, y))]
        white_bishops = [Piece('w', 'b', True, (2, y)),
                         Piece('w', 'b', True, (5, y))]
        white_queens = [Piece('w', 'q', True, (x1, y))]
        white_king = [Piece('w', 'k', True, (x2, y))]

        black_rooks = [Piece('b', 'r', True, (0, 7 - y)),
                       Piece('b', 'r', True, (7, 7 - y))]
        black_knights = [Piece('b', 'kn', True, (1, 7 - y)),
                         Piece('b', 'kn', True, (6, 7 - y))]
        black_bishops = [Piece('b', 'b', True, (2, 7 - y)),
                         Piece('b', 'b', True, (5, 7 - y))]
        black_queens = [Piece('b', 'q', True, (x1, 7 - y))]
        black_king = [Piece('b', 'k', True, (x2, 7 - y))]

        black_pieces = [black_king, black_pawns, black_bishops, black_rooks, black_queens, black_knights]
        white_pieces = [white_king, white_pawns, white_bishops, white_rooks, white_queens, white_knights]
        black = Player('b', pieces=black_pieces)
        white = Player('w', pieces=white_pieces)
        self.set_black(black)
        self.set_white(white)
        self.black.time_left = self.game_time
        self.white.time_left = self.game_time

    def reset(self):
        """
        reset the board
        :return: None
        """
        del self.white
        del self.black
        self.black = None
        self.white = None
        self.turn = 'w'
        self.last_move = None
        self.orientation = None
        self.draw = None
        self.started = False
        self.game_time = None
        self.ended = False

