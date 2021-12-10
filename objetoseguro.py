from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from base64 import b64encode, b64decode
from datetime import datetime

class ObjetoSeguro:
    def __init__(self, nombre:str):
        self.nombre = nombre
        self.keys = {}
        self.__gen_llaves()
        self.__logfile()

    def __gen_llaves(self):
        seed = Random.new().read
        self.__k_prv = RSA.generate(2048, seed)
        self.k_pub = self.__k_prv.publickey()

    def __logfile(self):
        self.__id = 0
        self.__file = self.nombre+".txt"
        f = open(self.__file, 'w')
        f.close()

    def saludar(self, destino:str, msg:str):
        return f"Hola {destino}: {self.__esperar_respuesta(msg)}"


    def __responder(self, msg:str):
        return "mensaje respuesta " + msg


    def consultar_msg(self, id):
        with open(self.__file, 'r') as f:
            data = f.readlines()
            for line in data:
                new_line = line.split(': ')
                if id == int(new_line[0]):
                    return new_line[1]
        return ""


    def cifrar_msg(self, k_pub, msg):
        cipher = PKCS1_OAEP.new(k_pub)
        return cipher.encrypt(self._codificar64(msg))


    def __decifrar_msg(self, msg):
        cipher = PKCS1_OAEP.new(self.__k_prv)
        return self._decodificar64(cipher.decrypt(msg))


    def llave_publica(self):
        return self.k_pub


    def _codificar64(self, msg):
        return b64encode(msg.encode("utf-8"))


    def _decodificar64(self, msg):
        return b64decode(msg).decode("utf-8")


    def almacenar_msg(self, msg):
        self.__id+=1
        with open(self.__file, 'a') as f:
            now = datetime.now()
            new_msg = msg + ": " + now.strftime("%d/%m/%Y, %H:%M:%S")
            f.write(f"{self.__id}: {new_msg}\n")
        return self.__id


    def __esperar_respuesta(self, msg):
        new_msg = self.__decifrar_msg(msg)
        self.almacenar_msg(new_msg)
        return self.__responder(new_msg)


if __name__ == '__main__':

    bob = ObjetoSeguro("Bob")
    alice = ObjetoSeguro("Alice")
    bob_saludo = bob.cifrar_msg(alice.llave_publica(), "hola mundo")
    print(alice.saludar(bob.nombre, bob_saludo))
    print(alice.consultar_msg(1))
    print(alice.almacenar_msg("adios"))
    print(alice.consultar_msg(3))
