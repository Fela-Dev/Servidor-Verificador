import json
from datetime import datetime
from modulos.validaciones_venta import Validaciones_Ventas
from conexion.consulta_registro_venta import Consultas_Ventas
class CampoIO:
    def __init__(self, valor="", status="", mensaje="d"):
        self.valor = valor
        self.status = None
        self.mensaje = mensaje
class RegistroVentaIO:
    def __init__(self):        
        self.id_cliente=CampoIO()
        
        self.numero_compra=CampoIO()
        self.fecha=CampoIO()
        self.num_tarjeta=CampoIO()
        self.fecha_vencimiento=CampoIO()
        self.codigo_tarjeta=CampoIO()
        self.total=CampoIO()
        #lista de productos
        self.lista_productos=[]

        self.datos_insert=[]

    def recibir_JSON(self,json):
        validaciones = Validaciones_Ventas()
        
        self.id_cliente=(json.get("Id_cliente"))
        self.numero_compra=(json.get("NumeroCompra")),
        self.fecha = datetime.strptime(json.get("Fecha"), "%Y-%m-%d").date()
        self.num_tarjeta = (json.get("NumeroTarjeta"))
        self.fecha_vencimiento=(json.get("FechaVencimiento"))
        self.total=(json.get("Total"))

        validaciones.validar_venta(self)
        #print("Usuario:", item["usuario"], "- Clave:", item["clave"])
        for item in json["ListaProductos"]:
            p = Producto(item["Codigo"],item["Cantidad"])

            self.lista_productos.append(p)
        
    def generar_datos_insert(self):
        self.datos_insert.append(self.id_cliente)
        self.datos_insert.append(self.fecha)
        self.datos_insert.append(self.total)
        self.datos_insert.append(0)
        pass
    def ejecutar_consulta(self):
        con_db=Consultas_Ventas()
        self.generar_datos_insert()
        con_db.insertar_venta(self.datos_insert, self.lista_productos)
        
        self.armar_respuesta()
    def armar_respuesta(self):
        respuesta="Todo se va bien por ahora"
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

class Producto:
    def __init__(self,codigo,cantidad):
        self.codigo=codigo
        self.cantidad=cantidad
