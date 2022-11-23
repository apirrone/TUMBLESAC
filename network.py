import pickle
import numpy as np
import time
import socket

from multiprocessing.connection import Client

class Network:
    def __init__(self, ip, port, name):
        self.__ip                  = ip
        self.__port                = port

        self.__id                  = None
        self.__name                = name
        self.__conn                = None

        self.__players             = {}
        self.__initial_board_state = None
        self.__game_over           = False

        self.__game_started        = False
        self.__i                   = 0
    
    def start(self):
        try:
            self.__conn = Client((self.__ip, self.__port))
        except ConnectionRefusedError as e:
            print(e)
            return False

        # first handshake, send my name and get my server_side id back
        msg = {"type" : "new_player", "name" : self.__name}
        self.__conn.send(msg)
        msg = self.__conn.recv()
        self.__id = msg["id"]

        return True

    def sendStartGame(self):
        msg = {"type" : "start_game"}
        self.__conn.send(msg)

    def sendReady(self, ready):
        msg = {"type" : "ready", "data" : ready}
        self.__conn.send(msg)

    def isGameStarted(self):
        return self.__game_started
    
    def isGameOver(self):
        return self.__game_over

    def sendWin(self):
        msg = {"type" : "win"}
        self.__conn.send(msg)

    def sendUpdate(self, boardState, charJPos):
        msg = {"type" : "send_update", "boardState" : boardState, "charJPos" : charJPos}
        self.__conn.send(msg)

    def disconnect(self):
        msg = {"type" : "disconnect"}
        self.__conn.send(msg)

    def getUpdate(self):
        msg = {"type" : "request_update", "tmp":self.__i }
        self.__i += 1
        self.__conn.send(msg)
        msg = self.__conn.recv()
        if msg["type"] == "game_update":
            self.__players = msg["data"]
            if not msg["game_started"] :
                if self.__initial_board_state is None:
                    self.__initial_board_state = msg["initial_board_state"]
                self.__game_started = False
            else:
                self.__game_started = True

        if msg["type"] == "game_over":
            winner = msg["data"]
            self.__game_over = True

    def getPlayers(self):
        return self.__players

    def getMyID(self):
        return self.__id

    def getMyName(self):
        return self.__name

    def getInitialBoardState(self):
        return self.__initial_board_state



# game_state = {"state" : np.array([1, 2, 3]), "bbc" : "aaa"}

# n = Network("localhost", 5001, "Antoijne")
# n.start()
# msg = game_state
# n.sendUpdate(msg)
# n.getUpdate()