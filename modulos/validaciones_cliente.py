
from email.utils import parseaddr

class Validaciones_Cliente:
    def ValidarCliente(self,cliente):
        self.validarCorreo(cliente)
        self.validarPais(cliente)

    def validarPais(self,cliente):
        if(cliente.pais.lenght==2):
            raise ValueError("El formato del pais no es correcto")
    
    def validarCorreo(self,cliente):
        nombre, direccion = parseaddr(cliente.correo)
        if "@" not in direccion:
            raise ValueError("El correo no es valido")