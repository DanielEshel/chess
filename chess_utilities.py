import chess_objects


def get_piece_on_square(place, pieces):
    """
    get piece on a given square
    :param place: coords of square
    :param pieces: pieces to search for
    :return: -1 if place is wrong, false if there's no piece and the piece object if found a piece
    """
    result = -1
    if place_on_board(place):
        for i in range(len(pieces)):
            for j in range(len(pieces[i])):
                if pieces[i][j].alive and pieces[i][j].place == place:
                    return pieces[i][j]
        result = False
    return result


def place_on_board(place):
    """
    check if a given place is on the board
    :param place: the board coordinates
    :return: bool of answer
    """
    if (place[0] in range(0, 8)) and (place[1] in range(0, 8)):
        return True
    return False


def checked(place_of_king, old_place_of_king, pieces_of_opponent, pieces_of_player, board_orientation):
    """
    check if king is checked (by place not piece -> checks if any piece threatens a given square)
    :param place_of_king: square coordinates to check (square the king wants to move to)
    :param old_place_of_king: place of king (before move)
    :param pieces_of_opponent: pieces of the opponent of the king
    :param pieces_of_player: pieces of the player that the king belongs to
    :param board_orientation: orientation of the board
    :return: false if king is not checked, piece object of piece checking if is checked
    """
    # check if knights are checking:
    piece_on_square = get_piece_on_square((place_of_king[0]+1, place_of_king[1]-2), pieces_of_opponent)
    if isinstance(piece_on_square, chess_objects.Piece) and piece_on_square.type == 'kn':
        return piece_on_square
    piece_on_square = get_piece_on_square((place_of_king[0]-1, place_of_king[1]-2), pieces_of_opponent)
    if isinstance(piece_on_square, chess_objects.Piece) and piece_on_square.type == 'kn':
        return piece_on_square
    piece_on_square = get_piece_on_square((place_of_king[0]+1, place_of_king[1]+2), pieces_of_opponent)
    if isinstance(piece_on_square, chess_objects.Piece) and piece_on_square.type == 'kn':
        return piece_on_square
    piece_on_square = get_piece_on_square((place_of_king[0]-1, place_of_king[1]+2), pieces_of_opponent)
    if isinstance(piece_on_square, chess_objects.Piece) and piece_on_square.type == 'kn':
        return piece_on_square
    piece_on_square = get_piece_on_square((place_of_king[0]+2, place_of_king[1]-1), pieces_of_opponent)
    if isinstance(piece_on_square, chess_objects.Piece) and piece_on_square.type == 'kn':
        return piece_on_square
    piece_on_square = get_piece_on_square((place_of_king[0]-2, place_of_king[1]-1), pieces_of_opponent)
    if isinstance(piece_on_square, chess_objects.Piece) and piece_on_square.type == 'kn':
        return piece_on_square
    piece_on_square = get_piece_on_square((place_of_king[0]+2, place_of_king[1]+1), pieces_of_opponent)
    if isinstance(piece_on_square, chess_objects.Piece) and piece_on_square.type == 'kn':
        return piece_on_square
    piece_on_square = get_piece_on_square((place_of_king[0]-2, place_of_king[1]+1), pieces_of_opponent)
    if isinstance(piece_on_square, chess_objects.Piece) and piece_on_square.type == 'kn':
        return piece_on_square

    # check if rook or queen are checking:
    for i in range(place_of_king[1]+1, 8):
        piece_on_square = get_piece_on_square((place_of_king[0], i), pieces_of_player + pieces_of_opponent)
        if isinstance(piece_on_square, chess_objects.Piece):
            if piece_on_square.color == pieces_of_opponent[0][0].color and \
                    (piece_on_square.type == 'r' or piece_on_square.type == 'q'):
                return piece_on_square
            elif piece_on_square.place != old_place_of_king:
                break
    for i in reversed(range(0, place_of_king[1])):
        piece_on_square = get_piece_on_square((place_of_king[0], i), pieces_of_player + pieces_of_opponent)
        if isinstance(piece_on_square, chess_objects.Piece):
            if piece_on_square.color == pieces_of_opponent[0][0].color and \
                    (piece_on_square.type == 'r' or piece_on_square.type == 'q'):
                return piece_on_square
            elif piece_on_square.place != old_place_of_king:
                break
    for i in range(place_of_king[0]+1, 8):
        piece_on_square = get_piece_on_square((i, place_of_king[1]), pieces_of_player + pieces_of_opponent)
        if isinstance(piece_on_square, chess_objects.Piece):
            if piece_on_square.color == pieces_of_opponent[0][0].color and \
                    (piece_on_square.type == 'r' or piece_on_square.type == 'q'):
                return piece_on_square
            elif piece_on_square.place != old_place_of_king:
                break
    for i in reversed(range(0, place_of_king[0])):
        piece_on_square = get_piece_on_square((i, place_of_king[1]), pieces_of_player + pieces_of_opponent)
        if isinstance(piece_on_square, chess_objects.Piece):
            if piece_on_square.color == pieces_of_opponent[0][0].color and \
                    (piece_on_square.type == 'r' or piece_on_square.type == 'q'):
                return piece_on_square
            elif piece_on_square.place != old_place_of_king:
                break

    # check if bishop or queen are checking:
    for i in range(place_of_king[0]+1, 8):
        piece_on_square = get_piece_on_square((i, i - place_of_king[0] + place_of_king[1]),
                                              pieces_of_player + pieces_of_opponent)
        if isinstance(piece_on_square, chess_objects.Piece):
            if piece_on_square.color == pieces_of_opponent[0][0].color and \
                    (piece_on_square.type == 'b' or piece_on_square.type == 'q'):
                return piece_on_square
            elif piece_on_square.place != old_place_of_king:
                break
    for i in reversed(range(0, place_of_king[0])):
        piece_on_square = get_piece_on_square((i, place_of_king[0] - i + place_of_king[1]),
                                              pieces_of_player + pieces_of_opponent)
        if isinstance(piece_on_square, chess_objects.Piece):
            if piece_on_square.color == pieces_of_opponent[0][0].color and \
                    (piece_on_square.type == 'b' or piece_on_square.type == 'q'):
                return piece_on_square
            elif piece_on_square.place != old_place_of_king:
                break
    for i in range(place_of_king[0]+1, 8):
        piece_on_square = get_piece_on_square((i, place_of_king[1] - (i - place_of_king[0])),
                                              pieces_of_player + pieces_of_opponent)
        if isinstance(piece_on_square, chess_objects.Piece):
            if piece_on_square.color == pieces_of_opponent[0][0].color and \
                    (piece_on_square.type == 'b' or piece_on_square.type == 'q'):
                return piece_on_square
            elif piece_on_square.place != old_place_of_king:
                break
    for i in reversed(range(0, place_of_king[0])):
        piece_on_square = get_piece_on_square((i, place_of_king[1] - (place_of_king[0] - i)),
                                              pieces_of_player + pieces_of_opponent)
        if isinstance(piece_on_square, chess_objects.Piece):
            if piece_on_square.color == pieces_of_opponent[0][0].color and \
                    (piece_on_square.type == 'b' or piece_on_square.type == 'q'):
                return piece_on_square
            elif piece_on_square.place != old_place_of_king:
                break

    # check if pawns are checking:
    if pieces_of_player[0][0].color == board_orientation:
        orientation = 1
    else:
        orientation = -1

    piece_on_square = get_piece_on_square((place_of_king[0] + 1, place_of_king[1] + orientation),
                                          pieces_of_opponent)
    if isinstance(piece_on_square, chess_objects.Piece) and piece_on_square.type == 'p':
        return piece_on_square

    piece_on_square = get_piece_on_square((place_of_king[0] - 1, place_of_king[1] + orientation),
                                          pieces_of_opponent)
    if isinstance(piece_on_square, chess_objects.Piece) and piece_on_square.type == 'p':
        return piece_on_square

    # if no one is checking, return False
    return False


def move(piece, place, board):
    """
    makes a move on the board
    :param piece: piece to move
    :param place: place to move to
    :param board: board to move on
    :return: returns bool if move is valid. if captured an opponent's piece, return the piece object
    """

    if not place_on_board(place):
        return False

    if piece:
        old_place_of_piece = piece.place
    else:
        return False

    if piece.color == board.orientation:
        orientation = 1
    else:
        orientation = -1
    if piece.color == 'w':
        pieces_of_player = board.white.pieces
        pieces_of_opponent = board.black.pieces
    else:
        pieces_of_player = board.black.pieces
        pieces_of_opponent = board. white.pieces

    # if theres already a friendly piece there
    if isinstance(get_piece_on_square(place, pieces_of_player), chess_objects.Piece):
        return False

    # get the piece on the square to move to
    piece_to_kill = get_piece_on_square(place, pieces_of_opponent)

    # check if pawn move is legal
    if piece.type == 'p':
        # if moves strait
        if place[0] == piece.place[0]:
            # if one square
            if place[1] == piece.place[1]+orientation:
                if piece_to_kill:
                    return False
            # if 2 squares
            elif piece.place[1] == orientation % 7 and place[1] == (3 * orientation) % 7:
                if piece_to_kill or \
                        isinstance(get_piece_on_square((place[0], place[1]-orientation),
                                                       pieces_of_opponent+pieces_of_player), chess_objects.Piece):
                    return False
            else:
                return False

        # if moves diagonally
        elif place[0] == piece.place[0] + 1 or place[0] == piece.place[0] - 1:
            if place[1] == piece.place[1]+orientation:
                # if there isn't a piece to kill, return False
                if not piece_to_kill:

                    # if it's an 'en passant'
                    if board.last_move is not None and (board.last_move[0].type == 'p') and \
                            (board.last_move[1][1] == board.last_move[0].place[1] + orientation*2) and \
                            (board.last_move[0].place[0] == place[0] and
                             board.last_move[0].place[1] == place[1] - orientation):
                        piece_to_kill = board.last_move[0]
                    else:
                        return False
            else:
                return False
        else:
            return False
        if place[1] == 0 or place[1] == 7:
            piece.type = 'q'

    # if piece if a rook, queen or bishop:
    elif piece.type == 'r' or piece.type == 'q' or piece.type == 'b':
        queen_flag = False
        # check rook moves
        if piece.type == 'r' or piece.type == 'q':
            if place[0] == piece.place[0]:
                if place[1] > piece.place[1]:
                    for i in range(piece.place[1]+1, place[1]):
                        if get_piece_on_square((place[0], i), pieces_of_player + pieces_of_opponent):
                            return False
                elif place[1] < piece.place[1]:
                    for i in range(place[1] + 1, piece.place[1]):
                        if get_piece_on_square((place[0], i), pieces_of_player + pieces_of_opponent):
                            return False
                else:
                    return False

            elif place[1] == piece.place[1]:
                if place[0] > piece.place[0]:
                    for i in range(piece.place[0]+1, place[0]):
                        if get_piece_on_square((i, place[1]), pieces_of_player + pieces_of_opponent):
                            return False
                elif place[0] < piece.place[0]:
                    for i in range(place[0] + 1, piece.place[0]):
                        if get_piece_on_square((i, place[1]), pieces_of_player + pieces_of_opponent):
                            return False
                else:
                    return False
            else:
                if piece.type == 'r':
                    return False
                else:
                    queen_flag = True

            piece.moved = True

        # check bishop moves
        if piece.type == 'b' or (piece.type == 'q' and queen_flag):
            # make sure the piece wants to move on a diagonal
            if place[0] == piece.place[0] or place[1] == piece.place[1]:
                return False
            if abs(piece.place[0] - place[0]) != abs(piece.place[1] - place[1]):
                return False

            # check that there aren't any pieces between the piece and the place it want's to move to
            if place[1] > piece.place[1]:
                if place[0] > piece.place[0]:
                    for i in range(piece.place[0] + 1, place[0]):
                        if get_piece_on_square((i, i - piece.place[0] + piece.place[1]),
                                               pieces_of_player + pieces_of_opponent):
                            return False
                else:
                    for i in reversed(range(place[0] + 1, piece.place[0])):
                        if get_piece_on_square((i, piece.place[0] - i + piece.place[1]),
                                               pieces_of_player + pieces_of_opponent):
                            return False

            else:
                if place[0] > piece.place[0]:
                    for i in reversed(range(piece.place[0] + 1, place[0])):
                        if get_piece_on_square((i, place[0] - i + place[1]),
                                               pieces_of_player + pieces_of_opponent):
                            return False
                else:
                    for i in range(place[0] + 1, piece.place[0]):
                        if get_piece_on_square((i, i - place[0] + place[1]),
                                               pieces_of_player + pieces_of_opponent):
                            return False

    # if knight move
    elif piece.type == 'kn':
        if ((place[0] == piece.place[0] + 1) and (place[1] == piece.place[1] + 2)) or \
                ((place[0] == piece.place[0] + 1) and (place[1] == piece.place[1] - 2)) or \
                ((place[0] == piece.place[0] - 1) and (place[1] == piece.place[1] + 2)) or \
                ((place[0] == piece.place[0] - 1) and (place[1] == piece.place[1] - 2)) or \
                ((place[0] == piece.place[0] + 2) and (place[1] == piece.place[1] + 1)) or \
                ((place[0] == piece.place[0] + 2) and (place[1] == piece.place[1] - 1)) or \
                ((place[0] == piece.place[0] - 2) and (place[1] == piece.place[1] + 1)) or \
                ((place[0] == piece.place[0] - 2) and (place[1] == piece.place[1] - 1)):
            pass
        else:
            return False

    elif piece.type == 'k':
        if isinstance(checked(place, piece.place, pieces_of_opponent, pieces_of_player,
                              board_orientation=board.orientation), chess_objects.Piece):
            return False
        if not checked(piece.place, piece.place, pieces_of_opponent, pieces_of_player,
                       board_orientation=board.orientation) and \
                not checked((place[0] - orientation, place[1]),
                            (place[0] - orientation, place[1]), pieces_of_opponent, pieces_of_player,
                            board_orientation=board.orientation):
            if piece.place[1] == place[1]:
                if not piece.moved:
                    if piece.place[0] == place[0] + 2:
                        for i in reversed(range(piece.place[0])):
                            piece_on_square = get_piece_on_square((i, place[1]), pieces_of_player + pieces_of_opponent)
                            if isinstance(piece_on_square, chess_objects.Piece):
                                if piece_on_square.type == 'r' and not piece_on_square.moved:
                                    piece_on_square.change_place((place[0] + 1, place[1]))
                                    piece.change_place(place)
                                    board.last_move = (piece, old_place_of_piece)
                                    return True
                                else:
                                    return False
                    elif piece.place[0] == place[0] - 2:
                        for i in range(piece.place[0] + 1, 8):
                            piece_on_square = get_piece_on_square((i, place[1]), pieces_of_player + pieces_of_opponent)
                            if isinstance(piece_on_square, chess_objects.Piece):
                                if piece_on_square.type == 'r' and not piece_on_square.moved:
                                    piece_on_square.change_place((place[0] - 1, place[1]))
                                    piece.change_place(place)
                                    board.last_move = (piece, old_place_of_piece)
                                    return True
                                else:
                                    return False

        # king can only move one square at a time
        if (place[0] not in range(piece.place[0]-1, piece.place[0] + 2)) or \
                (place[1] not in range(piece.place[1]-1, piece.place[1] + 2)):
            return False

        piece.moved = True

    # if there's a piece on the place to move to
    if isinstance(piece_to_kill, chess_objects.Piece):
        # kill the piece
        piece_to_kill.kill()
    # change the placement of the piece

    # move the piece
    piece.change_place(place)

    # if king is checked after the move
    if isinstance(checked(pieces_of_player[0][0].place, pieces_of_player[0][0].place,
                          pieces_of_opponent, pieces_of_player, board_orientation=board.orientation),
                  chess_objects.Piece):

        # return the piece to original place
        piece.change_place(old_place_of_piece)
        # revive the piece
        if isinstance(piece_to_kill, chess_objects.Piece):
            piece_to_kill.un_kill()
        # return False
        return False

    # if killed a piece, return it
    if isinstance(piece_to_kill, chess_objects.Piece):
        return piece_to_kill
    board.last_move = (piece, old_place_of_piece)
    return True


def check_block_of_check(piece, place, old_place, board):
    """
    check if the king is checked after a certain move without making the move
    :param piece: piece to check
    :param place: place to move to (place to check if checked after move)
    :param old_place: place to return the piece to
    :param board: board to check on
    :return: true if possible, false if not
    """

    # try to move
    piece_killed = move(piece=piece, place=place, board=board)

    # if killed a piece, revive it (we don't want to actually move)
    if piece_killed:
        if isinstance(piece_killed, chess_objects.Piece):
            piece_killed.un_kill()
        piece.change_place(old_place)
        return True

    return False


def king_can_move(king_of_opponent, board):
    """
    checks if the king of opponent can move (used to check draws and wins)
    :param king_of_opponent: king to check
    :param board: board to check on
    :return: bool if can move
    """
    # get pieces of player and pieces of opponent
    if king_of_opponent.color == 'w':
        pieces_of_player = board.black.pieces
        pieces_of_opponent = board.white.pieces
    else:
        pieces_of_player = board.white.pieces
        pieces_of_opponent = board. black.pieces

    x = king_of_opponent.place[0]
    y = king_of_opponent.place[1]

    # check every place (every square around the king)
    for i in range(8):
        if i in range(1):
            x += 1
        elif i in range(1, 2):
            y -= 1
        elif i in range(2, 4):
            x -= 1
        elif i in range(4, 6):
            y += 1
        elif i >= 6:
            x += 1
        # check if king can move to a different place (check all 8 squares)
        if not get_piece_on_square((x, y), pieces_of_opponent):
            if not checked(place_of_king=(x, y),
                           old_place_of_king=king_of_opponent.place,
                           pieces_of_opponent=pieces_of_player, pieces_of_player=pieces_of_opponent,
                           board_orientation=board.orientation):
                return True

    return False


def check_win_draw(king_of_opponent, board):
    """
    check if won the game
    :param king_of_opponent: king of opponent
    :param board: board to check on
    :return: bool if won or not
    """

    if king_of_opponent.color == 'w':
        pieces_of_player = board.black.pieces
        pieces_of_opponent = board.white.pieces
    else:
        pieces_of_player = board.white.pieces
        pieces_of_opponent = board. black.pieces

    if king_can_move(king_of_opponent, board):
        return False
    # check if any piece can block the check:
    for i in range(1, len(pieces_of_opponent)):
        for piece in pieces_of_opponent[i]:
            old_place = piece.place
            if piece.alive:
                # if piece checking if rook or queen
                if piece.type == 'r' or piece.type == 'q':
                    # check rook and queen moves:
                    for j in range(piece.place[1]+1, 8):
                        if check_block_of_check(piece, (piece.place[0], j), old_place=old_place, board=board):
                            return False
                        if isinstance(get_piece_on_square((piece.place[0], j), pieces_of_player + pieces_of_opponent),
                                      chess_objects.Piece):
                            break
                    for j in reversed(range(0, piece.place[1])):
                        if check_block_of_check(piece, (piece.place[0], j), old_place=old_place, board=board):
                            return False
                        if isinstance(get_piece_on_square((piece.place[0], j), pieces_of_player + pieces_of_opponent),
                                      chess_objects.Piece):
                            break
                    for j in range(piece.place[0]+1, 8):
                        if check_block_of_check(piece, (j, piece.place[1]), old_place=old_place, board=board):
                            return False
                        if isinstance(get_piece_on_square((j, piece.place[1]), pieces_of_player + pieces_of_opponent),
                                      chess_objects.Piece):
                            break
                    for j in reversed(range(0, piece.place[0])):
                        if check_block_of_check(piece, (j, piece.place[1]), old_place=old_place, board=board):
                            return False
                        if isinstance(get_piece_on_square((j, piece.place[1]), pieces_of_player + pieces_of_opponent),
                                      chess_objects.Piece):
                            break

                # if piece checking if bishop or queen
                if piece.type == 'b' or piece.type == 'q':
                    # check diagonal squares on lower x value
                    for j in reversed(range(0, piece.place[0])):
                        # check diagonal on lower y values
                        if check_block_of_check(piece, (j, piece.place[1]-(piece.place[0]-j)),
                                                old_place=old_place, board=board):
                            return False
                        # check diagonal of higher y values
                        if check_block_of_check(piece, (j, piece.place[1]+(piece.place[0]-j)),
                                                old_place=old_place, board=board):
                            return False
                        # if there's a on the square, break because the piece can't go further
                        if isinstance(get_piece_on_square((j, piece.place[1]-(piece.place[0]-j)),
                                                          pieces_of_player+pieces_of_opponent), chess_objects.Piece) or\
                            isinstance(get_piece_on_square((j, piece.place[1]+(piece.place[0]-j)),
                                                           pieces_of_player+pieces_of_opponent), chess_objects.Piece):
                            break

                    # check diagonal squares on higher x values
                    for j in range(piece.place[0] + 1, 8):
                        # check lower y values
                        if check_block_of_check(piece, (j, piece.place[1]-(j-piece.place[0])),
                                                old_place=old_place, board=board):
                            return False
                        # check higher y values
                        if check_block_of_check(piece, (j, piece.place[1]+(j-piece.place[0])),
                                                old_place=old_place, board=board):
                            return False
                        # if there's a on the square, break because the piece can't go further
                        if isinstance(get_piece_on_square((j, piece.place[1]-(j-piece.place[0])),
                                                          pieces_of_player+pieces_of_opponent), chess_objects.Piece) or\
                            isinstance(get_piece_on_square((j, piece.place[1]+(j-piece.place[0])),
                                                           pieces_of_player+pieces_of_opponent), chess_objects.Piece):
                            break

                elif piece.type == 'kn':
                    x = piece.place[0]
                    y = piece.place[1]
                    for j in range(8):
                        # change x, y values to cover all knight moves
                        if j == 0 or j == 1 or j == 7:
                            x += 1
                        if j == 0 or j == 6:
                            y += 2
                        if j == 1 or j == 3:
                            y -= 1
                        if j == 2:
                            y -= 2
                        if j == 3 or j == 5:
                            x -= 1
                        if j == 4:
                            x -= 2
                        if j == 5 or j == 7:
                            y += 1

                        # check if knight can move to (x, y)
                        if check_block_of_check(piece, (x, y), old_place=old_place, board=board):
                            return False

                elif piece.type == 'p':
                    # check every pawn move
                    x = piece.place[0]
                    y = piece.place[1]
                    if piece.color != board.orientation:
                        change = -1
                    else:
                        change = 1
                    if check_block_of_check(piece, (x, y+change), old_place=old_place, board=board):
                        return False
                    if check_block_of_check(piece, (x, y+2*change), old_place=old_place, board=board):
                        return False
                    if check_block_of_check(piece, (x-1, y+change), old_place=old_place, board=board):
                        return False
                    if check_block_of_check(piece, (x+1, y+change), old_place=old_place, board=board):
                        return False

    piece_checking = checked(place_of_king=(king_of_opponent.place[0], king_of_opponent.place[1]),
                             old_place_of_king=king_of_opponent.place,
                             pieces_of_opponent=pieces_of_player, pieces_of_player=pieces_of_opponent,
                             board_orientation=board.orientation)

    if isinstance(piece_checking, chess_objects.Piece):
        return 'W'
    return 'D'
