from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from base64 import b64encode, b64decode
hash = "SHA-256"

class ObjetoSeguro:
    def __init__(self, nombre):
        self.nombre = nombre
        self.__gen_llaves()

    def __gen_llaves(self):
        seed = Random.new().read
        self.k_prv = RSA.generate(2048, seed)
        self.k_pub = self.k_prv.publickey()

    def saludar(self, destino, msg):
        pass

    def _responder(self, msg):
        pass

    def consultar_msg():
        pass

    def cifrar_msg(self, k_pub, msg):
        cipher = PKCS1_OAEP.new(k_pub)
        return cipher.encrypt(self._codificar64(msg))

    def decifrar_msg(self, msg):
        cipher = PKCS1_OAEP.new(self.k_prv)
        return self._decodificar64(cipher.decrypt(msg))

    def llave_publica(self):
        return self.k_pub

    def _codificar64(self, msg):
        return b64encode(msg.encode("utf-8"))

    def _decodificar64(self, msg):
        return b64decode(msg).decode("utf-8")

    def _almacenar_msg(self, msg):
        pass

    def _esperar_respuesta(msg):
        print("waiting response")

if __name__ == '__main__':
    obj1 = ObjetoSeguro("Bob")
    cifrado = obj1.cifrar_msg(obj1.llave_publica(),"hola mundo")
    descifrado = obj1.decifrar_msg(cifrado)
    print(descifrado)
