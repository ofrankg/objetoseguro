from objetoseguro import ObjetoSeguro

if __name__ == '__main__':
    entity = ObjetoSeguro('Alice', 5051, 5050)
    entity.conectar()
    entity.start()
