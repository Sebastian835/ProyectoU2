class Personas:
    def __init__(self, nombre, apellido, correo, contraseña, cargo):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contraseña = contraseña
        self.cargo = cargo

    def toDBCollection(self):
        return{
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'contraseña': self.contraseña,
            'cargo': self.cargo,
        }
