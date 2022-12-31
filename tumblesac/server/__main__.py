import _thread
from multiprocessing.connection import Listener
import time
from tumblesac.board import Board
import sys


class Server:
    def __init__(self, ip, port, infinite=False):
        self.__ip = ip
        self.__port = port
        self.__infinite = infinite

        self.__current_id = 0
        self.__players = {}
        self.__connexions = {}

        self.__socket = Listener((self.__ip, self.__port))
        self.__board = Board((0, 0), nbColors=4, buffer_size=3, w=5)
        self.__boardSize = 50
        self.__board.populate(self.__boardSize)  # TODO choose this number well

        self.__game_started = False
        self.__game_ready = False

        self.__game_over = False
        self.__winner = None

    def __startGame(self):
        print("starting game")
        self.__game_ready = False
        self.__game_started = True
        self.__winner = None
        self.__game_over = False
        self.__board.populate(self.__boardSize)

    def __new_player(self, conn, id, name):
        print("New player ", name)
        self.__players[id] = {
            "name": name,
            "boardState": None,
            "charJPos": None,
            "ready": False,
            "score": 0,
        }
        conn.send({"id": id})

    def __disconnect(self, id):
        print("player ", self.__players[id]["name"], "disconnected")
        del self.__players[id]

    def __threaded_server(self, c, id):
        self.__connexions[id] = c
        first_handshake = True
        running = True
        while running:
            conn = self.__connexions[id]

            msg = conn.recv()

            if first_handshake:
                if msg["type"] == "new_player":
                    self.__new_player(conn, id, msg["name"])
                    first_handshake = False

            elif msg["type"] == "disconnect":
                self.__disconnect(id)
                running = False

            elif msg["type"] == "ready":
                ready = msg["data"]
                self.__players[id]["ready"] = ready
                if ready:
                    print("player ", self.__players[id]["name"], "is ready")
                else:
                    print("player ", self.__players[id]["name"], "is not ready")

            elif msg["type"] == "start_game":
                if self.__game_ready:
                    self.__startGame()

            elif msg["type"] == "win":
                self.__game_started = False
                self.__game_over = True
                self.__winner = self.__players[id]["name"]
                self.__players[id]["score"] += 1

            elif msg["type"] == "client_update":
                self.__players[id]["boardState"] = msg["boardState"]
                self.__players[id]["charJPos"] = msg["charJPos"]

            elif msg["type"] == "request_update":
                start = True
                for _, player in self.__players.items():
                    if not player["ready"]:
                        start = False
                        break

                if len(self.__players) == 0:
                    start = False

                self.__game_ready = start

                if not self.__game_started:
                    initial_board_state = self.__board.getState()
                    msg = {
                        "type": "game_update",
                        "data": self.__players,
                        "game_started": self.__game_started,
                        "game_over": self.__game_over,
                        "winner": self.__winner,
                        "initial_board_state": initial_board_state,
                    }
                else:
                    msg = {
                        "type": "game_update",
                        "data": self.__players,
                        "game_started": self.__game_started,
                        "game_over": self.__game_over,
                        "winner": self.__winner,
                    }
                    for _, player in self.__players.items():
                        player["ready"] = False
                conn.send(msg)

    def start(self):
        print("Waiting for connections ...")
        while True:
            c = self.__socket.accept()
            _thread.start_new_thread(self.__threaded_server, (c, self.__current_id))
            self.__current_id += 1
            time.sleep(0.1)


def mainInfinite():
    s = Server("0.0.0.0", 5001, infinite=True)
    s.start()


def mainNormal():
    s = Server("0.0.0.0", 5001)
    s.start()


if __name__ == "__main__":
    mainNormal()
