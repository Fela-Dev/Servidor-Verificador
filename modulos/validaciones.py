from entities.ClienteIO import ClienteIO
from email.utils import parseaddr
class Validaciones:
    def ValidarCliente(cliente):
        pass
    def validarPais(cliente):
        if(cliente.pais.lenght==2):
            raise ValueError("El formato del pais no es correcto")
    def validarCorreo(cliente):
        nombre, direccion = parseaddr(cliente.correo)
        if "@" not in direccion:
            raise ValueError("El correo no es valido")