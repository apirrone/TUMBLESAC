import socket

class Server:
    def __init__(self, ip, port):
        self.__ip   = ip
        self.__port = port

        self.__players = []

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.__ip, self.__port))
    
        print("Waiting for connections ...")
        self.__socket.listen()
        conn, addr = self.__socket.accept()


# TODO threaded server



# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)
