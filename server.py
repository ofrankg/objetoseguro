from concurrent.futures import ThreadPoolExecutor
import socket

class SocketServer:
    def __init__(self, puerto: int):
        self.client = None
        self.srvcon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port_and_ip = (socket.gethostname(), puerto)
        self.srv_thread = ThreadPoolExecutor(max_workers=3)
        self.msg = ""

    def accept(self):
        self.client, addr = self.srvcon.accept()

    def start(self):
        self.srvcon.bind(self.port_and_ip)
        self.srvcon.listen(5)
        return self.srv_thread.submit(self.accept)

    def read(self):
        while True:
            msg = self.client.recv(2048).decode()
            self.msg = msg
            if msg == "exit":
                break
            print(f">{msg}")

    def close(self):
        self.srvcon.shutdown(socket.SHUT_RDWR)
        self.srvcon.close()
