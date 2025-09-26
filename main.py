import socket
import os
import threading


from conexion.conexion_DB import Conexion_DB 
from entities.ClienteIO import ClienteIO
nucleos = os.cpu_count()
semaforo = threading.Semaphore(nucleos)

def manejar_cliente(client_socket, client_address):
    # Solo entra si hay "espacio" en el semáforo
    with semaforo:
        print(f"Conexión aceptada de {client_address}")

        try:
            cliente = ClienteIO()

            # Recibir datos
            data = client_socket.recv(1024).decode()
            print(f"Recibido del cliente: {data}")
            
            # Procesar informacion
            cliente.recibir_JSON(data)
            cliente.ejecutar_consulta()
            # consultas = Consultas_CLiente()
            # resultado = consultas.verificar(data)

            

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
    
    print(f"El equipo tiene {nucleos} núcleos.")
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

if __name__ == "__main__":
    main()
