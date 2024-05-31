######################################################################################
##   Asignatura: Programacion Paralela                                              ##
##   Entrega: Practica evaluable 1                                                  ##
##   Grupo: Jorge Rodriguez Navarro, Pepa Montero Jimena, Silvia Fernandez Villegas ##
######################################################################################
from multiprocessing import Process, Queue, Event
import os.path

## busqueda recibe una lista de paths hasta varios ficheros, el numero de procesos que vamos a crear
# el numero de datos que buscamos, y la condicion a cumplir por estos(una funcion)
def busqueda(datos:list, nr_buscadores:int, nr_datos_requeridos:int, condicion:callable):
    paths_q = Queue()
    results_q = Queue()
    n = len(datos)
    e = Event()
    
    ## Creamos la cola de paths a los archivos
    for i in range(n):
        paths_q.put(datos[i])
    
    for i in range(nr_buscadores):
        paths_q.put(None)
    
    ## Creamos la lista de procesos y los iniciamos
    procesos = [Process(target = buscador, args=(paths_q, results_q, condicion, e)) 
                for _ in range(nr_buscadores)]
    for p in procesos:
        p.start()
        
    # Hasta que la cola de entradas no este vacia nos quedamos en este bucle
    i = 0
    nombre_cond = condicion.__name__
    
    while not paths_q.empty():
    
        while not(results_q.empty()) and i < nr_datos_requeridos:
            i += 1
            dato = results_q.get()
            print(f"{i}: el numero: {dato[0]} satisface {nombre_cond} "
                    f"y esta en el archivo {dato[1]}")
        
        if i >= nr_datos_requeridos:#si hemos encontrado x datos
            e.set()#activamos el evento y salimos del bucle
            break

    for p in procesos:#Confirmamos que los procesos han acabado, por limpieza
        p.join()

"""    
    while not(results_q.empty()) and i < nr_datos_requeridos:
        i += 1
        dato = results_q.get()
        print(f"{i}: el numero: {dato[0]} satisface {nombre_cond} "
                f"y esta en el archivo {dato[1]}")
        
    if i >= nr_datos_requeridos:#si hemos encontrado x datos
        e.set()#activamos el evento y salimos del bucle
        break
"""

    if e.is_set():#si hemos encontrado suficientes datos los imprimimos 
        print(f"Se han encontrado {nr_datos_requeridos} datos que cumplen {nombre_cond}")
    
    else:# si no hemos encontrado suficientes datos lo decimos
        print(f"No se han encontrado {nr_datos_requeridos} datos que cumplan {nombre_cond}")

## Esta funcion es la que ejecuta cada proceso.
def buscador(input_q:Queue, output_q:Queue, condicion:callable, e:Event):
    path = input_q.get()
    
    while not(path is None):
        archivo = os.path.basename(path)#Me guardo el nombre del archivo
        
        ## Tratamos el archivo para pasarlo a una lista de numeros
        fd = open(path, "r")
        texto = fd.read()#si el path no es None, leemos el archivo
        fd.close()
        nums = list(map(int, texto.split()))#lo hacemos una lista
        n = len(nums)
        
        ## El buscador recorre el archivo y añade a la cola los elementos
        # que cumplan la condicion
        for i in range(n):
            
            if condicion(nums[i]):#si se cumple la condicion
                output_q.put((nums[i], archivo))#lo añadimos a la cola
            
            if e.is_set():#si el evento esta seteado el proceso se queda zombie
                return

        path = input_q.get()

### FUNCION CONDICION A CUMPLIR ########
def primo(n):
    
    for i in range(2, int(n**0.5)+1):
        
        if n % i == 0:
            return False
    
    return True

def primo_227(n:int):
    
    if primo(n) and (n % 1000) == 227:
        return True
    
    else:
        return False
########################################

if __name__ == "__main__":    
    nr_buscadores = 4
    nr_datos_requeridos = 3
    nr_archivos = 5
    
    l = [f'/home/jorgedebian/Documents/prueba/datos{i}' 
        for i in range(nr_archivos)]
#    l = ["/home/jorgedebian/Documents/prueba/prueba"]
    busqueda(l, nr_buscadores, nr_datos_requeridos, primo_227)
