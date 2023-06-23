
import time
import random
import chess_objects
import chess_utilities
from utilities import *


def start_game(ip1, ip2, game_manager, game_time):
    """
    starts a game between 2 clients
    :param ip1: first ip address
    :param ip2: second ip address
    :param game_manager: game manager
    :param game_time: wanted time for each player
    :return: none
    """

    # get the two players randomly
    white_player = chess_objects.Player(color='w', ip=random.choice([ip1, ip2]), time_left=(game_time * 600))
    if white_player.ip == ip1:
        black_player = chess_objects.Player(color='b', ip=ip2, time_left=game_time * 600)
    else:
        black_player = chess_objects.Player(color='b', ip=ip1, time_left=game_time * 600)

    # create a new board in the board list
    game_manager.boards.append(chess_objects.Board(white_player=white_player, black_player=black_player,
                                                   orientation='w'))
    # get player times
    game_manager.playing[ip1] = time.time()
    game_manager.playing[ip2] = time.time()
    # send players game starting msg
    game_manager.messages.append((white_player.ip, f"8{str(game_time).zfill(2)}w"))
    game_manager.messages.append((black_player.ip, f"8{str(game_time).zfill(2)}b"))


def end_game(board, game_manager):
    """
    ends a given game
    :param board: the board to close
    :param game_manager: game manager
    :return: none
    """

    # remove players from the playing list
    if board.white.ip in game_manager.playing.keys():
        del game_manager.playing[board.white.ip]
    if board.black.ip in game_manager.playing.keys():
        del game_manager.playing[board.black.ip]

    # remove board from board list
    game_manager.boards.remove(board)

    del board


def remove_client_data(ip, game_manager):
    """
    remove the data of the client from the server
    :param ip: ip of client
    :param game_manager: server's game manager
    :return: none
    """
    # remove from waiting list (if waiting)
    if ip in game_manager.waiting.values():
        del game_manager.waiting[get_key(ip, game_manager.waiting)]
    # remove from playing list (ifi playing)
    if ip in game_manager.playing.keys():
        board, player = get_player_board(ip, game_manager.boards)
        if player.color == 'w':
            opponent = board.black
        else:
            opponent = board.white
        # send resigning msg to the opponent
        game_manager.messages.append((opponent.ip, "3"))
        # close the game
        board.ended = True


def handle_disconnect_client(ip, game_manager):
    """
    disconnects a client and removes the client's data
    :param ip: address of client
    :param game_manager: data of clients
    :return: none
    """
    remove_client_data(ip, game_manager)

    # disconnect client communication
    game_manager.comm.disconnect_client(ip)


def get_player_board(ip, boards):
    """
    get the board that the player is playing on
    :param ip: player's address
    :param boards: all of the boards in the game
    :return: the board or none if isn't playing.
    """
    # for every board
    for board in boards:
        # if player is playing on the board, return it
        if ip == board.white.ip:
            return board, board.white
        elif ip == board.black.ip:
            return board, board.black


def handle_move(game_manager, ip, data):
    """
    make sure a move is valid and send it to the opponent
    :param game_manager: game manager
    :param ip: ip address of sender
    :param data: move data
    :return: None
    """
    # make sure that received data is appropriate
    if ip in game_manager.playing.keys() and len(data) == 5:

        board_info = get_player_board(ip, game_manager.boards)

        # make sure that board exists
        if board_info is not None:
            board, player = board_info

            # check if data is valid
            try:
                move = ((int(data[1]), int(data[2])), (int(data[3]), int(data[4])))
            except Exception as e:
                print('main_server - handle_msgs1', e)
                handle_disconnect_client(ip, game_manager)
            else:
                print(f"\tgot move: {move}\tfrom: {ip}\n")
                # get piece of square:
                if player.color == 'w':
                    opponent = board.black
                    piece = chess_utilities.get_piece_on_square(pieces=player.pieces, place=move[0])
                    place = move[1]
                else:
                    opponent = board.white
                    piece = chess_utilities.get_piece_on_square(pieces=player.pieces, place=(7 - move[0][0],
                                                                                             7 - move[0][1]))
                    place = (7 - move[1][0], 7 - move[1][1])

                if isinstance(piece, chess_objects.Piece):
                    # try to make the move on the server's board
                    if chess_utilities.move(piece=piece, place=place, board=board):
                        if not board.started:
                            board.started = True
                            game_manager.playing[player.ip] = time.time()
                        # if move was done with no error
                        # mirror the move for sending to the opponent
                        move_to_send = str(7 - move[0][0]) + str(7 - move[0][1]) + str(7-move[1][0]) + str(7-move[1][1])

                        # if there was a draw offered
                        if board.draw is not None and board.draw != player.color:
                            # send cancel draw msg to players if didn't offer the draw
                            board.draw = None
                            game_manager.messages.append((opponent.ip, '41'))
                            game_manager.messages.append((ip, '41'))

                        print(f"\tsent move: {move_to_send}\t to: {opponent.ip}\n")
                        game_manager.messages.append((opponent.ip, f'1{move_to_send}'))
                        board.last_move = piece, move[0]

                        # check for a win or draw after the move
                        win_draw = chess_utilities.check_win_draw(king_of_opponent=opponent.pieces[0][0], board=board)

                        # if its a win
                        if win_draw == 'W':
                            # send loosing msg to opponent
                            game_manager.messages.append((opponent.ip, '6'))
                            # send winning msg to player
                            game_manager.messages.append((ip, '5'))

                            # close the game 5
                            board.ended = True

                        # if its a draw
                        elif win_draw == 'D':
                            # send loosing msg to opponent
                            game_manager.messages.append((opponent.ip, '42'))
                            # send winning msg to player
                            game_manager.messages.append((ip, '42'))

                            # close the game 5
                            board.ended = True

                        else:
                            board.change_turn()
                            # send times to both players
                            game_manager.messages.append((player.ip,
                                                          f"9{str(player.time_left).zfill(5)[:5]}"
                                                          f"{str(opponent.time_left).zfill(5)[:5]}"))
                            game_manager.messages.append((opponent.ip,
                                                          f"9{str(opponent.time_left).zfill(5)[:5]}"
                                                          f"{str(player.time_left).zfill(5)[:5]}"))

                            # save the opponent's time
                            game_manager.playing[opponent.ip] = time.time()

                    else:
                        # if client sent an invalid move
                        handle_disconnect_client(ip, game_manager)
                else:
                    handle_disconnect_client(ip, game_manager)


