from conexion.conexion_DB import Conexion_DB as con_db

class Consultas_Ventas:
    def __init__(self):
        self.con_db = con_db
    def existen_prodcutos(lista_prodcutos):
        pass
    def insertar_venta(self,lista_datos,lista_productos):
        print("Mi lista ")
        print(type(lista_datos[0]))
        print(type(lista_datos[1]))
        print(type(lista_datos[2]))

        sp_name="sp_insertar_factura"
        num_f=con_db.ejecutar_con_retorno(sp_name,lista_datos)
        self.insertar_detalle_venta(num_f,lista_productos)
    def insertar_detalle_venta(self,num_f,lista_productos):
        for i in lista_productos:
            datos_p=[]
            datos_p.append(i.codigo)
            datos_p.append(i.cantidad)
            datos_p.append(num_f[3])
            print(datos_p)
            query = "CALL sp_insertar_detalle(%s, %s, %s)"
            con_db.ejecutar_sin_retorno(query,(datos_p))
            pass