import os
import psutil

class Config:
    ip_puerto="localhost"
    puerto_clientes_ventas="6666"
    
    
    guia_comandos="""
    Lista de de funciones del servidor
    segun el numero de comando recibido
    1.Insertar Cliente
    2.Actulizar Cliente
    3.Borrar Cliente
    4.Consultar CLiente
    5.Realizar  Factura
    """
    def info_sistema(self):
        

        # Número de núcleos
        nucleos = os.cpu_count()

        # RAM total en GB
        ram_total = psutil.virtual_memory().total / (1024 ** 3)

        # RAM disponible en GB
        ram_disponible = psutil.virtual_memory().available / (1024 ** 3)

        # String multilínea con la info
        guia_sistema = f"""
        Información del sistema:

        - Núcleos disponibles: {nucleos}
        - RAM total: {ram_total:.2f} GB
        - RAM disponible: {ram_disponible:.2f} GB
        """

        print(guia_sistema)