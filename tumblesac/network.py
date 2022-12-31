from multiprocessing.connection import Client
import requests
import json
import threading


class Network:
    def __init__(self, cfg_file_path):

        cfg = json.load(open(cfg_file_path))

        self.__ip = cfg["ip"]
        self.__port = cfg["port"]
        self.__name = cfg["name"]
        self.__game_type = None
        self.__seed = None

        self.__id = None
        self.__conn = None

        self.__players = {}
        self.__initial_board_state = None
        self.__game_over = False
        self.__winner = None

        self.__game_started = False

        self.__sent_win = False

        self.__sendUpdateTimeout = 0
        self.__getUpdateTimeout = 0

        self.__highscoresUrl = "https://api.jsonbin.io/v3/b/63a6f7e115ab31599e23fef8"
        self.__highscoresHeaders = {
            "X-ACCESS-KEY": "$2b$10$hxyg4xmjB.IUyB6uaeFAOukAHDS71v1u4.jx6kHn9vAR4YqMFMh8i"
        }

        self.__updating = False
        self.__lastScore = 0

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
        self.__game_type = msg["game_type"]
        print("GAME TYPE :", self.__game_type)

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

    def sendUpdate(self, boardState, charJPos, dt):
        if self.__sendUpdateTimeout > 0:
            self.__sendUpdateTimeout -= dt
            return
        msg = {"type": "client_update", "boardState": boardState, "charJPos": charJPos}
        self.__conn.send(msg)
        self.__sendUpdateTimeout = 0.1

    def disconnect(self):
        if self.__conn is not None:
            msg = {"type": "disconnect"}
            self.__conn.send(msg)

    def getUpdate(self, dt):
        if self.__getUpdateTimeout > 0:
            self.__getUpdateTimeout -= dt
            return

        msg = {"type": "request_update"}
        self.__conn.send(msg)
        msg = self.__conn.recv()
        if msg["type"] == "game_update":
            self.__players = msg["data"]
            if not msg["game_started"]:
                if self.__initial_board_state is None:
                    self.__initial_board_state = msg["initial_board_state"]
                    self.__seed = msg["seed"]
                self.__game_started = False
            else:
                self.__game_started = True

            self.__game_over = msg["game_over"]
            self.__winner = msg["winner"]
        self.__getUpdateTimeout = 0.1

    def getPlayers(self):
        return self.__players

    def getMyID(self):
        return self.__id

    def getMyName(self):
        return self.__name

    def getPort(self):
        return self.__port

    def getSeed(self):
        return self.__seed

    def isInfinite(self):
        return self.__game_type == "infinite"

    def getInitialBoardState(self):
        return self.__initial_board_state

    def getHighScores(self):

        highscores = json.loads(
            requests.get(
                self.__highscoresUrl + "/latest",
                json=None,
                headers=self.__highscoresHeaders,
            ).text
        )["record"]

        return highscores

    def updateHighScores(self, score):
        self.__lastScore = score
        self.__updating = True
        t = threading.Thread(target=self.t_updateHighScores, args=(score,))
        t.start()

    def t_updateHighScores(self, score):
        print("UPDATING HIGHSCORES ... ")
        highscores = self.getHighScores()
        if self.__name in highscores:
            if score > int(highscores[self.__name]):
                highscores[self.__name] = score
        else:
            highscores[self.__name] = score

        requests.put(
            self.__highscoresUrl, json=highscores, headers=self.__highscoresHeaders
        )
        print("DONE !")
        self.__updating = False

    # To test
    def getNHighestScores(self, n=3):
        highscores = self.getHighScores()
        sorted_highscores = sorted(
            highscores.items(), key=lambda item: item[1], reverse=True
        )
        return sorted_highscores[:n]

    def isUpdating(self):
        return self.__updating

    def getLastScore(self):
        return self.__lastScore
