from threading import Lock

# Esta clase es un set con un lock.
# Va a servir para llevar cuenta de las claves que estan siendo usadas
class LockedSet:
    def __init__(self):
        self.keys = set()# Esto tengo que cambiarlo por un set
        self.lk = Lock()
    
    def add(self, clave):
        self.lk.acquire()
        if not(clave in self.keys):
            self.keys.add(clave)
            self.lk.release()
            return True
        else:
            self.lk.release()
            return False

    def erase(self, clave):
        self.lk.acquire()
        self.keys.discard(clave)
        self.lk.release()

# La clase base de datos. Tiene metodos para dar de alta, baja, consultar, y modificar entradas
# Consiste en un diccionario con un LockedSet
class BaseDeDatos:
    def __init__(self):
        self.db = dict()
        self.keys = LockedSet()
    
    def alta(self, nombre, info):
        if self.keys.add(nombre):
            if nombre in self.db:
                self.keys.erase(nombre)
                return(f"Ya existe una entrada {nombre} en la base de datos. Cambie el registro")
        
            else:
                self.db[nombre] = info
                self.keys.erase(nombre)
                return(f"Nueva entrada {nombre} creada con informacion {info}")
        else:
            return ("Esta entrada esta ocupada, prueba de nuevo mas tarde")
    
    def baja(self, nombre):
        if self.keys.add(nombre):
            try:
                del(self.db[nombre])
                self.keys.erase(nombre)
                return(f"Entrada {nombre} eliminada")
            except KeyError:
                self.keys.erase(nombre)
                return(f"Entrada {nombre} no existe")
        else:
            return(f"Entrada {nombre} esta ocupada, prueba de nuevo mas tarde")

            
    def modificacion(self, nombre, info):
        if self.keys.add(nombre):
            try:
                self.db[nombre] = info
                self.keys.erase(nombre)
                return(f"Entrada {nombre} modificada a {info}")
            except KeyError:
                self.keys.erase(nombre)
                return(f"Entrada {nombre} no existe, pruebe a darla de alta primero")
        else:
            return (f"Entrada {nombre} esta ocupada, prueba de nuevo mas tarde")

    def consulta(self, nombre):
        if self.keys.add(nombre):
            try:
                result = self.db[nombre]
                self.keys.erase(db)
                return(f"Entrada {nombre} tiene asociado {info}")
            except KeyError:
                self.keys.erase(db)
                return(f"No existe una entrada {nombre} en la base de datos")
        else:
            return(f"Entrada {nombre} esta ocupada, prueba de nuevo mas tarde")

