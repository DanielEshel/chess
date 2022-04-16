from client_com import ClientComm
import queue
import threading
import chess_objects
import chess_utilities
from client_objects import Graphics


def handle_msgs(recv_q, board, ended):
    """
    handle the data received from the server
    :param recv_q: queue of msgs
    :param board: game's board
    :param ended: if session has ended
    :return: None
    """
    while True:
        # if program ended
        if not ended.empty():
            break

        # if theres data
        if not recv_q.empty():
            data = recv_q.get()

            # if got game-starting message from server
            if data[0] == '8':

                # get color of player
                board.orientation = data[3]

                # get game time
                try:
                    game_time = int(data[1:3])
                except Exception as e:
                    print(str(e), "server error")
                    exit()
                else:
                    board.game_time = game_time*600

            else:
                # if got other data, wait for the game-data
                while board.orientation is None:
                    pass

                # get player and opponent
                if board.orientation == 'w':
                    player = board.white
                    opponent = board.black

                else:
                    player = board.black
                    opponent = board.white

                # if got move of opponent
                if data[0] == '1':
                    # get pieces.
                    opponent_pieces = opponent.pieces

                    opponent_move = data[1:]
                    try:
                        opponent_move = ((int(opponent_move[0]), int(opponent_move[1])), (int(opponent_move[2]),
                                                                                          int(opponent_move[3])))
                    except Exception as e:
                        print(str(e))
                        print(opponent_move)
                        exit()
                    piece_to_move = chess_utilities.get_piece_on_square(pieces=opponent_pieces, place=opponent_move[0])

                    if chess_utilities.move(piece=piece_to_move, board=board, place=opponent_move[1]):
                        if not board.started:
                            board.started = True
                        board.turn = board.orientation
                        Graphics.print_game()
                    else:
                        print("exited because move of opponent is invalid")
                        exit()

                # if server sent times
                elif data[0] == '9':
                    if len(data) == 11:
                        try:
                            player.time_left = int(data[1:6])
                            opponent.time_left = int(data[6:])
                        except Exception as e:
                            print(str(e), "server error")
                            exit()
                    else:
                        print("sever error")
                        exit()

                # if got resignation msg
                elif data[0] == '3':
                    if board.started:
                        board.ended = 'You won: opponent resigned!'
                    else:
                        board.ended = 'Opponent aborted!'

                # if draw-related
                elif data[0] == '4':
                    # received draw request
                    if data[1] == '0':
                        board.draw = 'R'
                    # received draw declination
                    elif data[1] == '1':
                        board.draw = 'C'
                    # received draw
                    elif data[1] == '2':
                        board.ended = 'Draw!'

                # if got wining msg
                elif data[0] == '5':
                    board.ended = 'You won by check mate!'

                # if got loosing msg
                elif data[0] == '6':
                    board.ended = 'Opponent won by check mate!'

                # if game ended on time
                elif data[0] == '7':
                    if data[1] == '0':
                        board.ended = 'You won: opponent ran out of time!'
                    else:
                        board.ended = 'You lost: you ran out of time!'


def handle_graphic_input(board, input_q, comm, ended):
    """
    handle the graphic input from the user (button presses)
    :param board: game's board
    :param input_q: queue of input from the user
    :param comm: communication object
    :param ended: if session has ended
    :return: None
    """
    while True:

        # if program ended
        if not ended.empty():
            break

        # if got board info for the first time (game started), initialize the pieces of the board
        if board.orientation is not None:
            if board.black is None:
                board.init_pieces()

        # if got any data in the input queue (cant be blocking)
        if not input_q.empty():
            # get data
            data = input_q.get()

            # if got move from user
            if data[0] == 'M':
                comm.send(f'1{data[1:]}')
                board.change_turn()

            # if username selected game_mode
            elif data[0] == 'P':
                # get wanted game time
                game_time = data[1:]
                # send wanted time to server
                comm.send(f"8{game_time}")

            # if aborted or resigned game
            elif data == 'R' or data == 'A':
                comm.send('3')

            # if draw
            elif data[0] == 'D':
                # if accepted/offered draw
                if data[1] == 'A' or data[1] == 'O':
                    comm.send("40")
                # if declined/canceled draw
                elif data[1] == 'C':
                    comm.send("41")

            # if exited game waiting
            elif data == 'EGW':
                # send exit game waiting message
                comm.send(f"800")


def main():

    server_ip = '172.105.68.55'

    # get pieces
    board = chess_objects.Board()

    recv_q = queue.Queue()
    input_q = queue.Queue()
    start = ['t']

    # if program ended
    ended = queue.Queue()

    comm = ClientComm(server_ip, 1234, recv_q, start)

    # start user and server input threads
    threading.Thread(target=handle_msgs, args=(recv_q, board, ended)).start()
    threading.Thread(target=handle_graphic_input, args=(board, input_q, comm, ended)).start()

    # main thread of graphics (pygame)
    Graphics(input_q, board, start)

    # if graphics has ended, change ended to close threads
    ended.put(True)
    # close the communication
    comm.close()
    print("\n\nbye bye")


if __name__ == '__main__':
    main()
