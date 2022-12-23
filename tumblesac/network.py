from multiprocessing.connection import Client


class Network:
    def __init__(self, ip, port, name):
        self.__ip = ip
        self.__port = port

        self.__id = None
        self.__name = name
        self.__conn = None

        self.__players = {}
        self.__initial_board_state = None
        self.__game_over = False
        self.__winner = None

        self.__game_started = False

        self.__sent_win = False

    def start(self):
        try:
            self.__conn = Client((self.__ip, self.__port))
        except ConnectionRefusedError as e:
            print(e)
            return False

        # first handshake, send my name and get my server_side id back
        msg = {"type": "new_player", "name": self.__name}
        self.__conn.send(msg)
        msg = self.__conn.recv()
        self.__id = msg["id"]

        return True

    def reset(self):
        self.__winner = None
        self.__game_started = False
        self.__game_over = False
        self.__initial_board_state = None
        self.__sent_win = False

    def sendStartGame(self):
        msg = {"type": "start_game"}
        self.__conn.send(msg)

    def sendReady(self, ready):
        msg = {"type": "ready", "data": ready}
        self.__conn.send(msg)

    def isGameStarted(self):
        return self.__game_started

    def isGameOver(self):
        return self.__game_over, self.__winner

    def sendWin(self):
        msg = {"type": "win"}
        self.__conn.send(msg)
        self.__sent_win = True

    def winSent(self):
        return self.__sent_win

    def sendUpdate(self, boardState, charJPos):
        msg = {"type": "client_update", "boardState": boardState, "charJPos": charJPos}
        self.__conn.send(msg)

    def disconnect(self):
        if self.__conn is not None:
            msg = {"type": "disconnect"}
            self.__conn.send(msg)

    def getUpdate(self):
        msg = {"type": "request_update"}
        self.__conn.send(msg)
        msg = self.__conn.recv()
        if msg["type"] == "game_update":
            self.__players = msg["data"]
            if not msg["game_started"]:
                if self.__initial_board_state is None:
                    self.__initial_board_state = msg["initial_board_state"]
                self.__game_started = False
            else:
                self.__game_started = True

            self.__game_over = msg["game_over"]
            self.__winner = msg["winner"]

    def getPlayers(self):
        return self.__players

    def getMyID(self):
        return self.__id

    def getMyName(self):
        return self.__name

    def getInitialBoardState(self):
        return self.__initial_board_state
