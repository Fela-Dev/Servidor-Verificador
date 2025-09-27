import socket
import os
import threading
import json

from conf import Config
from conexion.conexion_DB import Conexion_DB 
from entities.ClienteIO import ClienteIO
nucleos = os.cpu_count()
semaforo = threading.Semaphore(nucleos)
def inicio_servidor():

    config = Config()
    print(config.guia_comandos)

    config.info_sistema()
    
    print("Inicio sistema de verificación")

    # Conectar a la base de datos
    con = Conexion_DB()
    con.conectar()

    # Crear socket del servidor solo una vez
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 6666))
    server_socket.listen(10)
    print("Servidor escuchando en localhost:6666...")

    while True:
        # Aceptar conexión
        client_socket, client_address = server_socket.accept()
        

        # Crear hilo para manejar al cliente

        hilo = threading.Thread(target=manejar_cliente, args=(client_socket, client_address))
        hilo.start()

def manejar_cliente(client_socket, client_address):
    # Solo entra si hay "espacio" en el semáforo
    with semaforo:
        print(f"Conexión aceptada de {client_address}")

        try:
            

            
            

            data = client_socket.recv(1024).decode()
            print(f"Recibido del cliente: {data}")

            # Convertir string JSON a diccionario
            data_json = json.loads(data)

            tipo_solicitud = data_json.get("op_code")

            if tipo_solicitud <= 1 or tipo_solicitud <= 3:
                cliente = ClienteIO()
                # Procesar información
                cliente.recibir_JSON(data)   # <-- ahora le pasas un dict
                cliente.ejecutar_consulta()
                # consultas = Consultas_CLiente()
                            # resultado = consultas.verificar(data)
            elif(tipo_solicitud==5):
                cliente = ClienteIO()
                cliente.mensaje="Funcion insertar factura aun no implmentada"
            else:
                cliente = ClienteIO()
                cliente.mensaje=(f"comando {tipo_solicitud} no corresponde a ninguna funcionalidad")

            

        except Exception as e:
            cliente.armar_respuesta_error(str(e))
            print(f"Error con {client_address}: {e}")

        finally:
            #Enviar respuesta
            mensaje=cliente.mensaje
            client_socket.send(mensaje.encode())
            client_socket.close()
            print(f"Conexión con {client_address} cerrada")

def main():
    
    inicio_servidor()

if __name__ == "__main__":
    main()
