import mysql.connector#py -m pip install mysql-connector-python
from mysql.connector import Error

class Conexion_DB:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = '1234'
    DATABASE = 'db_verificador'

    conexion = None

    @classmethod
    def conectar(cls):
        try:
            cls.conexion = mysql.connector.connect(
                host=cls.HOST,
                user=cls.USER,
                password=cls.PASSWORD,
                database=cls.DATABASE
            )
            if cls.conexion.is_connected():
                print("Conexión a MySQL a realizada")
        except Error as e:
            raise ValueError(f"Error conectando a MySQL: {e}")
    @classmethod
    def cerrar(cls):
        if cls.conexion and cls.conexion.is_connected():
            cls.conexion.close()
            cls.conexion = None
            print("Conexión cerrada")
    
    @classmethod
    def ejecutar_sin_retorno(cls, query, parametros=None):
        cursor = None
        try:
            print("->", query, "<-")
            cursor = cls.conexion.cursor()
            # En mysql-connector los parámetros van como %s
            cursor.execute(query, parametros or [])
            cls.conexion.commit()
            return True
        except Exception as e:
            if cls.conexion.in_transaction:  
                cls.conexion.rollback()
            raise ValueError(f"Error ejecutando query: {e}")
        finally:
            if cursor:
                cursor.close()
    
    @classmethod
    def ejecutar_con_retorno(cls, sp_name, parametros=None):
        """
        Ejecuta un stored procedure que devuelve valores mediante parámetros OUT.
        :param sp_name= nombre del stored procedure
        :param parametros: lista de parámetros, incluso NOne
        :return: lista de valores de los parámetros qu regresa el sp
        """
        cursor = None
        try:
            cursor = cls.conexion.cursor()
            # Llamada al stored procedure
            result_params = cursor.callproc(sp_name, parametros or [])
            cls.conexion.commit()
            return result_params  # Devuelve la lista con valores actualizados, incluyendo OUT
        except Exception as e:
            if cls.conexion.in_transaction:
                cls.conexion.rollback()
            raise ValueError(f"Error ejecutando stored procedure: {e}")
        finally:
            if cursor:
                cursor.close()


