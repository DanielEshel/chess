class Manager:
    def __init__(self, comm, boards, playing, waiting, messages):
        """
        initialize game manager
        :param comm: communication object
        :param usernames: dictionary of usernames by ip address
        :param boards: list of boards
        :param playing: dictionary of playing players (and last time remaining sample)
        :param waiting: dictionary of player waiting for a game by wanted time of game
        :param messages: list of messages to send to clients
        """
        self.boards = boards
        self.playing = playing
        self.waiting = waiting
        self.comm = comm
        self.messages = messages

    def send_messages(self):
        """
        sends every waiting message
        :return: none
        """
        # for every message in the list
        messages_copy = list(self.messages)
        for msg in messages_copy:
            # get the socket and the msg of every item in the list
            (ip, message) = msg
            # print(f'ip: {ip}, msg: {message}')
            self.comm.send(str(len(message)).zfill(2) + message, ip)
            self.messages.remove(msg)

