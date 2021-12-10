from objetoseguro import ObjetoSeguro

if __name__ == '__main__':
    # Creacion de objetos
    bob = ObjetoSeguro("Bob")
    alice = ObjetoSeguro("Alice")

    # Crear mensaje cifrado de bob con llave de alice
    bob_saludo = bob.cifrar_msg(alice.llave_publica(), "hola mundo")

    # Alice saluda a Bob
    print(alice.saludar(bob.nombre, bob_saludo))

    # Consulta de mensajes de alice
    print(alice.consultar_msg(1))

    # Almacenar mensaje en log de alice
    print(alice.almacenar_msg("adios"))

    # Consultar mensaje no existente
    print(alice.consultar_msg(3))
