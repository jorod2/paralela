class BaseDeDatos:
    def __innit__(self):
        self.db = dict()
    
    def alta(self, nombre, info):
        if nombre in self.db:
            return(f"Ya existe una entrada {nombre} en la base de datos. Cambie el registro",flush = True)
        
        else:
            self.d[nombre] = info
            return(f"Nueva entrada {nombre} creada", flush = True)
    
    def baja(self, nombre):
        try:
            del(self.db[nombre])
            return(f"Entrada {nombre} eliminada", flush = True)
        except KeyError:
            return(f"{nombre} no existe en la base de datos",flush = True)
            
    def modificacion(self, nombre, info):
        if nombre in self.db:
            self.db[nombre] = info
            return(f"Entrada {nombre} modificada", flush = True)
        else:
            return(f"Entrada {nombre} no existe",flush = True)
    
    
    def consulta(self, nombre):
        try:
            return(f"En la base de datos{nombre} tiene asociado {self.db[nombre]}", flush = True)
        except KeyError:
            return(f"No existe una entrada {nombre} en la base de datos",flush = True)
