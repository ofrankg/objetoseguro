from concurrent.futures import ThreadPoolExecutor
import logging
import socket

class SocketClient:
    def __init__(self, puerto: int):
        self.clicon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port_and_ip = (socket.gethostname(), puerto)
        self.cli_thread = ThreadPoolExecutor(max_workers=4)
        self.msg = ""

    def conecta(self):
        while True:
            try:
                self.clicon.connect(self.port_and_ip)
                break
            except ConnectionRefusedError:
                pass

    def start(self):
        return self.cli_thread.submit(self.conecta)

    def send_msg(self, msg):
        self.clicon.send(msg.encode())
        if msg != "exit":
            self.msg = ""

    def write(self):
        while self.msg != "exit":
            if self.msg == "":
                pass
            else:
                self.send_msg(self.msg)

    def captura_msg(self, texto):
        self.msg = texto

    def close(self):
        self.clicon.shutdown(socket.SHUT_RDWR)
        self.clicon.close()
