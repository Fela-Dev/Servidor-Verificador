import json
from conexion.consultas_cliente import Consultas_CLiente 
class CampoIO:
    def __init__(self, valor="", status="", mensaje=""):
        self.valor = valor
        self.status = None
        self.mensaje = mensaje

class ClienteIO:
    def __init__(self):
        self.tipoMantenimiento = CampoIO()
        self.cedula = CampoIO()
        self.pais = CampoIO()
        self.nombre = CampoIO()
        self.primerApellido = CampoIO()
        self.segundoApellido = CampoIO()
        self.correo = CampoIO()
        self.telefono = CampoIO()
        self.direccion = CampoIO()
        

    def recibir_JSON(self, json_str):
        # Convierte el string JSON a diccionario
        try:
            datos = json.loads(json_str)
            self.json=datos#<- guarda e dicioanrio json en un atributo
        except json.JSONDecodeError:
            raise ValueError("JSON no válido")
        
        print("📦 JSON recibido:")
        print(json.dumps(datos, indent=4, ensure_ascii=False))

        # Asigna los valores recibidos a cada atributo
        self.tipoMantenimiento.valor =(datos.get("op_code", ""))
        self.cedula.valor = datos.get("Cedula", "")
        self.pais.valor = datos.get("Pais", "")
        self.nombre.valor = datos.get("Nombre", "")
        self.primerApellido.valor = datos.get("PrimerApellido", "")
        self.segundoApellido.valor = datos.get("SegundoApellido", "")
        self.correo.valor = datos.get("Correo", "")
        self.telefono.valor = datos.get("Telefono", "")
        self.direccion.valor = datos.get("Direccion", "")
    def generar_lista(self):
        """
        lista de etributos:Funciones de consulta
        a la db, reciben lso parametros en forma de lista
        """

        return [
            self.tipoMantenimiento.valor,
            self.cedula.valor,
            self.pais.valor,
            self.nombre.valor,
            self.primerApellido.valor,
            self.segundoApellido.valor,
            self.correo.valor,
            self.telefono.valor,
            self.direccion.valor
        ]
    def ejecutar_consulta(self):
        con_cliente = Consultas_CLiente()
        
        con_cliente.mantenimiento_cliente(self.generar_lista())#eejcuta consulta
        self.armar_respuesta()
        

    def armar_respuesta(self):
        print("El tipo es")
        print(type(self.tipoMantenimiento))


        if self.tipoMantenimiento.valor == 1:
            respuesta = "Nuevo cliente ingresado con éxito"
        elif self.tipoMantenimiento.valor == 2:
            respuesta = "Cliente actualizado correctamente"
        elif self.tipoMantenimiento.valor == 3:
            respuesta = "Cliente eliminado exitosamente"
        else:
            respuesta = "Tipo de mantenimiento no reconocido"

        respuesta = {
            "status": "OK",
            "mensaje": respuesta
        }
        self.mensaje = json.dumps(respuesta, indent=4, ensure_ascii=False)
    
    def armar_respuesta_error(self,respuesta):
        respuesta = {
            "status": "ERROR",
            "mensaje": respuesta
        }
        self.mensaje = json.dumps(respuesta, indent=4, ensure_ascii=False)
    def validar():
        pass

