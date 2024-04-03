from threading import Lock


class LockedDict:
    def __innit__(self):
        self.dict = dict()
        self.lk = Lock()
        
    def add(self, key):
        if key in self.dict: # Se supone que esta operacion es atomica en CPython. Entiendo que
            return False      # dependera del interprete usado
        else:
            self.lk.acquire()
            try:
                self.dict[key] = 0
            except KeyError:
                return False
            self.lk.release()
            return True

    def ocupar(self, key):
        if key in self.dict:
            self.lk.acquire()
            self.dict[key] = 0
            try:
                self.dict[key] = 0
            except KeyError:
                return False
            self.lk.release()
            return True
        else:
            return False
            
    def liberar(self, key):
        if key in self.dict:
            self.lk.acquire()
            try:
                self.dict[key] = 1
            except KeyError:
                return False
            self.lk.release()
            return True
        else:
            return False
    
    def borrar(self, key):
        if key in self.dict:
            self.lk.acquire()
            del(self.dict[key])
            self.lk.release()
            return True
        else:
            return False
    
    def estado(self, key):
        try:
            self.lk.acquire(blocking=False)
            result = self.dict[key]
            self.lk.release()
            return result
        except KeyError:
            return("Esta entrada no existe")



class BaseDeDatos:
    def __innit__(self):
        self.db = dict()
        self.keys = LockedDict()
    
    def alta(self, nombre, info):
        
        if nombre in self.keys:
            return(f"Ya existe una entrada {nombre} en la base de datos. Cambie el registro")
        
        else:
            self.keys.add(nombre)
            self.db[nombre] = info
            self.keys.liberar(nombre)
            return(f"Nueva entrada {nombre} creada")
    
    def baja(self, nombre):
        if nombre in self.keys:
            while !(self.keys.consultar(nombre)): #Mientras que esto no este libre
                pass
            self.keys.borrar(nombre)
            del(self.db[nombre])
            return(f"Entrada {nombre} eliminada")
        else:
            return(f"Entrada {nombre} no existe")
            
    def modificacion(self, nombre, info):
        if nombre in self.keys:
            while !(self.keys.consultar(nombre)):
                pass
            self.keys.ocupar(nombre)
            try:
                self.db[nombre] = info
            except KeyError:
                return(f"Entrada {nombre} no existe")
            self.keys.liberar(nombre)
            return(f"Entrada {nombre} modificada")
        else:
            return(f"Entrada {nombre} no existe")
    
    
    def consulta(self, nombre):
        if nombre in self.keys:
            while !(self.keys.estado(nombre)):
                pass
            self.keys.ocupar(nombre)
            try:
                result = self.db[nombre]
            except KeyError:
                return(f"No existe una entrada {nombre} en la base de datos")
            self.keys.liberar(nombre)
            return(f"En la base de datos{nombre} tiene asociado {result}")
        else:
            return(f"No existe una entrada {nombre} en la base de datos")
