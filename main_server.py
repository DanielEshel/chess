from server_utils import *
from server_com import ServerComm
import queue
import threading
from server_objects import Manager
import time


def handle_msgs(recv_q, game_manager):
    """
    handle the messages received from the clients
    :param recv_q: message queue
    :param game_manager: game manager
    :return: None
    """
    while True:
        ip, data = recv_q.get()

        request_number = data[0]

        if request_number == '1':
            # client sent a move
            handle_move(game_manager, ip, data)

        elif request_number in ['3', '4']:
            # client resigned a game
            if ip in game_manager.playing.keys():

                # get board and player
                board, player = get_player_board(ip, game_manager.boards)

                # get opponent
                if player.color == 'w':
                    opponent = board.black
                else:
                    opponent = board.white

                # if client sent resigned
                if request_number == '3':
                    # send resigning msg to the opponent
                    game_manager.messages.append((opponent.ip, '3'))

                    # end the game
                    board.ended = True

                # if client offered a draw
                elif request_number == '4':
                    if len(data) == 2:
                        # if offered a draw
                        if data[1] == '0':
                            # check if opponent wants a draw too
                            if board.draw == opponent.color:
                                # send draw msg to the players and end the game
                                game_manager.messages.append((opponent.ip, "42"))
                                game_manager.messages.append((ip, "42"))
                                board.ended = True
                            else:
                                # send draw offer to the opponent
                                board.draw = player.color
                                game_manager.messages.append((opponent.ip, '40'))
                        elif data[1] == '1':
                            # if canceled the draw, send draw cancellation and reset status
                            board.draw = None
                            game_manager.messages.append((opponent.ip, '41'))
                            game_manager.messages.append((ip, '41'))

        elif request_number == '8':
            # client sent game request
            if len(data) == 3:
                try:
                    wanted_time = int(data[1:])
                except Exception as e:
                    # if client didn't  send msg according to protocol
                    print("main_server - handle_msgs - request_number=8", e)
                    handle_disconnect_client(ip, game_manager)
                else:
                    if wanted_time in [30, 15, 10, 5, 3, 2, 1]:
                        # if there's another player waiting (make sure same client doesnt play against himself)
                        if wanted_time in game_manager.waiting.keys() and game_manager.waiting[wanted_time] != ip:
                            start_game(ip, game_manager.waiting[wanted_time], game_manager, wanted_time)
                            del game_manager.waiting[wanted_time]
                        else:
                            game_manager.waiting[wanted_time] = ip
                    elif wanted_time == 0:
                        # get game time of waiting player
                        game_time = get_key(ip, game_manager.waiting)
                        # if in the waiting list, delete it
                        if game_time is not None:
                            del game_manager.waiting[game_time]


def main():
    recv_q = queue.Queue()
    comm = ServerComm(1234, recv_q)
    game_manager = Manager(comm=comm, boards=[], playing={}, waiting={}, messages=[])
    threading.Thread(target=handle_msgs, args=(recv_q, game_manager, )).start()

    while True:

        # handle disconnected clients
        for i in range(len(comm.disconnected_clients)):
            remove_client_data(comm.disconnected_clients[i], game_manager)
        comm.disconnected_clients = []

        # deal with players' times
        for board in game_manager.boards:

            # check if game has ended
            if board.ended:
                end_game(board=board, game_manager=game_manager)
                continue

            # handle time if board has started
            if board.started:

                if board.turn == 'w':
                    player = board.white
                    opponent = board.black
                else:
                    player = board.black
                    opponent = board.white

                time_passed = time.time() - game_manager.playing[player.ip]

                if time_passed >= 0.1:
                    # decrease playing player's time
                    player.time_left -= int(time_passed * 10)
                    game_manager.playing[player.ip] = time.time()

                # check if lost on time
                if player.time_left <= 0:
                    game_manager.messages.extend([(player.ip, "71"), (opponent.ip, "70")])
                    end_game(board=board, game_manager=game_manager)

            game_manager.send_messages()

        # send messages to clients
        game_manager.send_messages()


if __name__ == '__main__':
    main()
