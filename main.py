import socket
import os
import threading
import json

from conf import Config
from conexion.conexion_DB import Conexion_DB 

from entities.ClienteIO import ClienteIO
from entities.RegistroVenta import RegistroVentaIO
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
                solicitud_cliente = ClienteIO()
                # Procesar información
                solicitud_cliente.recibir_JSON(data_json)   # <-- ahora le pasas un dict
                solicitud_cliente.ejecutar_consulta()
                # consultas = Consultas_CLiente()
                # resultado = consultas.verificar(data)
            elif(tipo_solicitud==5):
                solicitud_cliente = RegistroVentaIO()
                solicitud_cliente.recibir_JSON(data_json)
                solicitud_cliente.ejecutar_consulta() 
                
                #solicitud_cliente.mensaje="Funcion insertar factura aun no implmentada"
            else:
                solicitud_cliente = ClienteIO()
                solicitud_cliente.mensaje=(f"comando {tipo_solicitud} no corresponde a ninguna funcionalidad")

            

        except Exception as e:
            solicitud_cliente.armar_respuesta_error(str(e))
            print(f"Error con {client_address}: {e}")

        finally:
            #Enviar respuesta
            mensaje=solicitud_cliente.mensaje
            client_socket.send(mensaje.encode())
            client_socket.close()
            print(f"Conexión con {client_address} cerrada")

def main():
    
    inicio_servidor()

if __name__ == "__main__":
    main()
