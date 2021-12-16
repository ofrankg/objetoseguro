from objetoseguro import ObjetoSeguro

if __name__ == '__main__':
    entity = ObjetoSeguro('Bob', 5050, 5051)
    entity.conectar()
    entity.start()
