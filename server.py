# import socket
import _thread
from multiprocessing.connection import Listener
import time
from board import Board


class Server:
    def __init__(self, ip, port):
        self.__ip           = ip
        self.__port         = port

        self.__current_id   = 0
        self.__players      = {}
        self.__connexions   = {}

        self.__socket       = Listener((self.__ip, self.__port))
        self.__board        = Board((0, 0), nbColors=6, buffer_size=3, w=5)
        self.__board.populate(150) # TODO choose this number well

        self.__game_started = False
        self.__game_ready   = False

        self.__game_over    = False

        self.__sessions     = {}

    def __new_player(self, conn, id, name):
        print("New player ", name)
        self.__players[id] = {"name" : name, "boardState" : None, "charJPos" : None, "ready" : False}
        conn.send({"id" : id})

    def __disconnect(self, id):
        print("player ", self.__players[id]["name"], "disconnected")
        del self.__players[id]


    # TODO handle disconnections properly
    def __threaded_server(self, conn, id):
        self.__connexions[id] = conn
        first_handshake = True
        running = True
        while running:

            # conn = self.__connexions[id] -> this causes ran out of input
            try:
                msg = conn.recv()
            except Exception as e:
                print(e)
                pass

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
                    self.__game_started = True

            elif msg["type"] == "win":
                msg = {"type" : "game_over", "data" : None}
                self.__game_over = True
                conn.send(msg)                

            elif msg["type"] == "send_update":
                self.__players[id]["boardState"] = msg["boardState"]
                self.__players[id]["charJPos"] = msg["charJPos"]

            elif msg["type"] == "request_update":
                i = msg["tmp"]
                start = True
                for id, player in self.__players.items():
                    if not player["ready"]:
                        start = False
                        break

                if len(self.__players) == 0:
                    start = False
                
                self.__game_ready = start
                if not self.__game_started:
                    initial_board_state = self.__board.getState()
                    msg = {"type" : "game_update", "data" : self.__players, "game_started" : self.__game_started, "initial_board_state" : initial_board_state}
                else:
                    msg = {"type" : "game_update", "data" : self.__players, "game_started" : self.__game_started}

                conn.send(msg)




    def start(self):
        print("Waiting for connections ...")
        while True:
            conn = self.__socket.accept()
            _thread.start_new_thread(self.__threaded_server, (conn, self.__current_id))
            self.__current_id += 1
            time.sleep(0.1)

s = Server("0.0.0.0", 5001)
s.start()