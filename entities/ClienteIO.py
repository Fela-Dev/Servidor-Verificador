import json
from modulos.validaciones_cliente import Validaciones_Cliente
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
        

    def recibir_JSON(self, json):
        validaciones = Validaciones_Cliente()
        # Convierte el string JSON a diccionario
        
        
        # Asigna los valores recibidos a cada atributo
        self.tipoMantenimiento.valor =(json.get("op_code", ""))
        self.cedula.valor = json.get("Cedula", "")
        self.pais.valor = json.get("Pais", "")
        self.nombre.valor = json.get("Nombre", "")
        self.primerApellido.valor = json.get("PrimerApellido", "")
        self.segundoApellido.valor = json.get("SegundoApellido", "")
        self.correo.valor = json.get("Correo", "")
        self.telefono.valor = json.get("Telefono", "")
        self.direccion.valor = json.get("Direccion", "")
        # valida datos
        validaciones.ValidarCliente(self)
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

