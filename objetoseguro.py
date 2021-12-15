'''
    Archivo: objetoseguro.py
    Autor: Oswaldo Franco
    Fecha: Diciembre 2021
    Programa: INTEL-INAOE 2021
'''
# bibliotecas para uso de esquemas de cifrado
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from base64 import b64encode, b64decode
from datetime import datetime
from server import SocketServer
from client import SocketClient
from concurrent.futures import ThreadPoolExecutor

'''
Atributos:
    self.nombre: nombre de objeto
    self.__k_prv: llave privada de esquema RSA
    self.k_pub: llave publica de esquema RSA
    self.__id: identificador de mensaje
    self.__file: nombre de archivo log
'''

class ObjetoSeguro:
    def __init__(self, nombre: str, puerto_srv: int, puerto_cli: int):
        self.nombre = nombre
        self.srv_socket = SocketServer(puerto_srv)
        self.cli_socket = SocketClient(puerto_cli)
        self.messenger = ThreadPoolExecutor(max_workers=3)
        self.__gen_llaves()
        self.__logfile()

    def __gen_llaves(self):
        seed = Random.new().read
        self.__key = RSA.generate(2048, seed)
        self.k_prv = self.__key.exportKey()
        self.k_pub = self.__key.publickey().exportKey()

    def __logfile(self):
        self.__id = 0
        self.__file = self.nombre+".txt"
        f = open(self.__file, 'w')
        f.close()

    def saludar(self, destino: str, msg: str):
        return f"Hola {destino}: {self.__esperar_respuesta(msg)}"

    def __responder(self, msg: str):
        return "mensaje respuesta " + msg

    def consultar_msg(self, id: int):
        with open(self.__file, 'r') as f:
            data = f.readlines()
            for line in data:
                new_line = line.split(': ')
                if id == int(new_line[0]):
                    return new_line[1]
        return ""

    def cifrar_msg(self, k_pub: bytes, msg: str):
        cipher = PKCS1_OAEP.new(RSA.importKey(k_pub))
        return cipher.encrypt(self._codificar64(msg))

    def decifrar_msg(self, msg):
        cipher = PKCS1_OAEP.new(RSA.importKey(self.k_prv))
        return self._decodificar64(cipher.decrypt(msg))

    def llave_publica(self):
        return self.k_pub

    def _codificar64(self, msg):
        return b64encode(msg.encode("utf-8"))

    def _decodificar64(self, msg):
        return b64decode(msg).decode("utf-8")

    def almacenar_msg(self, msg: str):
        self.__id += 1
        now = datetime.now()
        new_msg = msg + ": " + now.strftime("%d/%m/%Y, %H:%M:%S")
        with open(self.__file, 'a') as f:
            f.write(f"{self.__id}: {new_msg}\n")
        return self.__id

    def __esperar_respuesta(self, msg):
        new_msg = self.__decifrar_msg(msg)
        self.almacenar_msg(new_msg)
        return self.__responder(new_msg)

    def conectar(self):
        server = self.srv_socket.start()
        client = self.cli_socket.start()
        while not server.done() and not client.done():
            pass
        print("Conectado")

    def start(self):
        self.write = self.messenger.submit(self.cli_socket.write)
        self.read = self.messenger.submit(self.srv_socket.read)

        # self.cli_socket.captura_msg(self.k_pub)
        # self.llave_cliente = self.srv_socket.llave
        # print(self.llave_cliente)

        self.messenger.submit(self.send_msg)

    def send_msg(self):
        while True:
            msg = input()
            self.cli_socket.captura_msg(msg)
