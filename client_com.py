import socket
import threading


class ClientComm:
    """
    class to represent client (communication)
    """
    def __init__(self, server_ip, port, msg_q, start):
        """
        init the opject
        :param server_ip: server ip address
        :param port: port of communication
        :param msg_q: que for messages
        """
        self.socket = None
        self.server_ip = server_ip
        self.port = port
        self.q = msg_q
        self.start = start
        self.exit = False
        threading.Thread(target=self._main_loop).start()

    def _main_loop(self):
        """
        connects to server
        :return:
        """
        # build socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

        while True:
            try:
                length = int(self.socket.recv(2).decode())
            except Exception as e:
                if self.exit:
                    exit()
                else:
                    print('ClientCom - _main_loop2', str(e))
                    self.start[0] = 'f'
                    self.socket.close()
                    self.socket = None
                    self.connect()

            else:
                try:
                    data = self.socket.recv(length).decode()
                except Exception as e:
                    if self.exit:
                        exit()
                    print('clientcom - _main_loop3', str(e))
                    self.start[0] = 'f'
                    self.socket.close()
                    self.socket = None
                    self.connect()
                else:
                    print(f"\t\tgot data: {data}")
                    self.q.put(data)

    def connect(self):
        # try to connect to server
        if self.socket is None:
            self.socket = socket.socket()

        while True:
            # if started (or tried reconnecting)
            if self.start[0] == 't':
                print("start is t")
                try:
                    self.socket.connect((self.server_ip, self.port))
                except Exception as e:
                    if self.exit:
                        exit()
                    self.start[0] = 'f'
                    print('clientComm - _main_loop1' + str(e))
                else:
                    self.start[0] = 's'
                    break

            if self.exit:
                exit()

    def send(self, msg):
        """
        sends a given msg in the object's socket
        :param msg: the msg to send
        :return:
        """
        if type(msg) == str:
            msg = str(len(msg)).zfill(2) + msg
            msg = msg.encode()
        try:
            self.socket.send(msg)
        except Exception as e:
            if self.exit:
                exit()
            print(f'ClientComm - send\nmsg: {msg}' + str(e))
            self.start[0] = 'f'
            self.socket.close()
            self.socket = None
            self.connect()

    def close(self):
        self.socket.close()
        self.exit = True


