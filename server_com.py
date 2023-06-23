import socket
import threading
import select


class ServerComm:
    """
    class to represent client (communication)
    """
    def __init__(self, port, msg_q):
        """
        init the communication object
        :param port: port of communication
        :param msg_q: que for messages
        """
        self.socket = None
        self.port = port
        self.q = msg_q
        self.open_clients = {}
        self.disconnected_clients = []
        threading.Thread(target=self._main_loop).start()

    def _main_loop(self):
        """
        connects to server
        :return: none
        """
        self.socket = socket.socket()
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(3)

        while True:
            rlist,wlist,xlist = select.select([self.socket]+list(self.open_clients.keys()),
                                              list(self.open_clients.keys()), [])
            for current_socket in rlist:
                if current_socket is self.socket:
                    client, addr = self.socket.accept()
                    print(f"{addr} - connected")
                    self.open_clients[client] = addr[0]
                else:
                    # get length of msg
                    try:
                        msg_length = current_socket.recv(2).decode()
                        msg_length = int(msg_length)
                    except Exception as e:
                        print('ServerComm - _main_loop1', str(e))
                        self._disconnect_client(current_socket)

                    else:
                        # if client disconnected:
                        if msg_length == '':
                            self._disconnect_client(current_socket)
                        elif msg_length > 16:
                            self._disconnect_client(current_socket)
                        else:
                            # check that client is still sending
                            if self._client_in_read_list(current_socket):
                                try:
                                    data = current_socket.recv(msg_length).decode()
                                except Exception as e:
                                    print('ServerComm - _main_loop2', str(e))
                                    self._disconnect_client(current_socket)
                                else:
                                    # if client disconnected:
                                    if data == '':
                                        self._disconnect_client(current_socket)
                                    else:
                                        print(f"got data: {data}")
                                        self.q.put((self.open_clients[current_socket], data))
                            # if client stopped sending when it should have, disconnect the client.
                            else:
                                self._disconnect_client(current_socket)

    def _client_in_read_list(self, client_socket):
        """
        checks if client is still sending data
        :param client_socket: socket to check
        :return: bool
        """
        # make sure that client is still sending
        if client_socket not in select.select([self.socket] + list(self.open_clients.keys()),
                                              list(self.open_clients.keys()), [])[0]:
            return False
        return True

    def _disconnect_client(self, socket_to_disconnect):
        """
        disconnect client
        :param socket_to_disconnect: client socket to disconnect
        :return: none
        """
        if socket_to_disconnect in self.open_clients:
            # add client to disconnected list
            self.disconnected_clients.append(self.open_clients[socket_to_disconnect])

            print(f"{self.open_clients[socket_to_disconnect]} - disconnected")
            if socket_to_disconnect in self.open_clients.keys():
                del self.open_clients[socket_to_disconnect]
                socket_to_disconnect.close()

    def disconnect_client(self, ip):
        """
        disconnects a client (public function)
        :param ip: ip address of client
        :return: none
        """
        soc = self._get_socket(ip)
        self._disconnect_client(soc)

    def _get_socket(self, ip):
        """
        return the matching socket of an ip address
        :param ip: the ip address
        :return: matching socket, return false if there's no matching socket.
        """
        result = False
        for soc in self.open_clients:
            if self.open_clients[soc] == ip:
                result = soc
                break
        return result

    def send(self, msg, ip):
        """
        send msg to a client
        :param msg: the message to send
        :param ip: ip address to send to
        :return: none
        """
        # encode msg if needed
        if type(msg) == str:
            msg = msg.encode()

        # get matching socket
        soc = self._get_socket(ip)

        # if there's a matching socket, send the message
        if soc is not False:
            try:
                soc.send(msg)
                print(f"\treally sent: {msg.decode()}")
            except Exception as e:
                # disconnect the client if there's an error
                print(f'ServerCom - send\nmsg: {msg.decode()}', str(e))
                self._disconnect_client(soc)
