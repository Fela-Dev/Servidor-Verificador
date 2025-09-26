from conexion.conexion_DB import Conexion_DB as con_db

class Consultas_CLiente:
    def __init__(self):
        self.con_db = con_db
    def mantenimiento_cliente(self,datos_cliente):
        
        query = "CALL sp_mantenimiento_clientes(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.con_db.ejecutar_sin_retorno(query,(datos_cliente))
