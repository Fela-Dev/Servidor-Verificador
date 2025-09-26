import pyodbc
from datetime import datetime
class Conexion_DB:
    SERVER = 'MSI'
    DATABASE = 'SuperTico'

    @classmethod
    def obtener_cadena_conexion(cls,usuario,contra):
        cls.usuario=usuario
        
        cls.cadena_conexion = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={cls.SERVER};"
        f"DATABASE={cls.DATABASE};"
        f"UID={usuario};"
        f"PWD={contra}"
        )
        print(cls.cadena_conexion)

    @classmethod
    def get_cadena_conexion(cls):
        return cls.cadena_conexion
    @classmethod
    def validar_cadena_conexion(cls):
        try:
            cls.conexion = pyodbc.connect(cls.cadena_conexion)
            print(cls.conexion)
        
            return True
        except Exception as e:
            raise ValueError(e)
    
    @classmethod  
    def verificar_usuario_en_tabla(cls):
        query = "EXEC verificar_existencia_usuario @usuario = ?"
        resultado = cls.ejecutar_una_fila(query, (cls.usuario,))
        
        if resultado is not None and resultado[0] > 0:
            cls.id_usuario=resultado[1]
            return True
        else:
            raise ValueError("Usuario con permiso en SQL, pero no registrado en la tabla de la base de datos.")



    @classmethod
    def ejecutar_sin_retorno(cls, query, parametros=None):
        cursor = None
        try:
            print("->",query,"<-")
            cursor = cls.conexion.cursor()
            cursor.execute(query, parametros or [])
            cls.conexion.commit()
            
            return True
        except Exception as e:
            cls.conexion.rollback()
            raise ValueError(e)
            
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def ejecutar_una_fila(cls, query, parametros=None):
        print("->",query,"<-")
        print("Tipo/>",type(parametros))

        cursor = None
        try:
            cursor = cls.conexion.cursor()
            cursor.execute(query, parametros or [])
            return cursor.fetchone()
        except Exception as e:
            raise ValueError(e)
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def ejecutar_varias_filas(cls, query, parametros=None):
        cursor = None
        try:
            cursor = cls.conexion.cursor()
            cursor.execute(query, parametros or [])
            return cursor.fetchall()
        except Exception as e:
            raise ValueError(e)
        finally:
            if cursor:
                cursor.close()
    @classmethod
    def ejecutar_multiples_resultados(cls, query, parametros=None):
        cursor = None
        try:
            cursor = cls.conexion.cursor()
            cursor.execute(query, parametros or [])

            resultados = []

            while True:
                if cursor.description:  # solo si el SELECT devuelve columnas
                    filas = cursor.fetchall()
                    resultados.append(filas)

                if not cursor.nextset():
                    break

            return resultados

        except Exception as e:
            raise ValueError(f"Error ejecutando query: {e}")
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def insertar_audiroria(cls,id_tipo_auditoria):
        ahora = datetime.now()
        fecha_actual = ahora.date()
        hora_actual = ahora.time()
       
        datos=[]
        datos.append(cls.id_usuario)
        datos.append(id_tipo_auditoria)
        datos.append(fecha_actual)
        datos.append(hora_actual)

        
        qwery="sp_insertar_auditoria @id_usuario=?,@id_auditoria=?,@fecha=?,@hora=?"
        cls.ejecutar_sin_retorno(qwery,(datos))

        