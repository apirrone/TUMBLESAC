# import socket
import _thread
from multiprocessing.connection import Listener
import time
from board import Board


class Server:
    def __init__(self, ip, port):
        self.__ip           = ip
        self.__port         = port

        self.__players      = {}
        self.__connexions   = {}

        self.__socket       = Listener((self.__ip, self.__port))
        self.__board        = Board((0, 0))
        self.__board.populate(30) # TODO choose this number well

        self.__game_started = False

    def __threaded_server(self, conn, id):
        self.__connexions[id] = conn
        first_handshake = True
        running = True
        while running:
            conn = self.__connexions[id]
            try:
                msg = conn.recv()
            except Exception as e:
                pass
            if first_handshake:
                if msg["type"] == "new_player":
                    name = msg["name"] 
                    self.__players[id] = {"name" : name, "boardState" : None, "charJPos" : None}
                    conn.send({"id" : id})
                    first_handshake = False
            elif msg["type"] == "start_game":
                self.__game_started = True
            elif msg["type"] == "is_game_started":
                initial_board_state = self.__board.getState()
                if not self.__game_started:
                    conn.send({"is_game_started": False, "initial_board_state" : initial_board_state})
                else:
                    conn.send({"is_game_started": True, "initial_board_state" : initial_board_state})
            elif msg["type"] == "win":
                msg = {"type" : "game_over", "data" : None}
                conn.send(msg)                
            elif msg["type"] == "send_update":
                self.__players[id]["boardState"] = msg["boardState"]
                self.__players[id]["charJPos"] = msg["charJPos"]
            elif msg["type"] == "request_update":
                msg = {"type" : "game_update", "data" : self.__players}
                conn.send(msg)


    def start(self):
        print("Waiting for connections ...")
        while True:
            conn = self.__socket.accept()
            _thread.start_new_thread(self.__threaded_server, (conn, len(list(self.__players.keys()))))
            time.sleep(0.1)

s = Server("0.0.0.0", 5001)
s.start()