import basedatos
from socket import socket
from threading import Thread, active_count


### Funcion para registrar la entrada del cliente ###
def separador_strings(msg:str):
    
    for i in range(len(msg)):
        
        if msg[i] == ' ':
            return msg[:i], msg[i+1:]
    
    return msg, ""
#####################################################

def entrada_db(info:str):
    for i in range(len(info)):
        if info[i] == ":"
            return info[:i], msg[i+1:]
    return info[:i], ""

#Funcion que parsea el futuro value de la base de datos. Devuelve la tupla vacia si encuentr aun error
def value(msg:str):
    n = len(msg)
    if msg[0] == '(' and msg[n] == ')':
        l = msg[1:n-1].split(,)
        try:
            int(l[0])
            tuple(l)
                return tuple(l)
            else:
                return tuple()
        except ValueError:
            return tuple()##Input no valido
    else:
        return tuple()##Input no valido
    
### Funciones de soporte para el servidor ###
def alta(db, nombre, info):
    return db.alta(nombre, info)

def baja(db, nombre):
    return db.baja(nombre)

def modificacion(db, nombre, info):
    return db.modificacion(nombre, info)

def consulta(db, nombre):
    return db.consulta(nombre)
############################################

## Funcion objetivo para las hebras
def ft_server(cl_socket, ,db):
    msj_rec = cl_socket.recv(1024)
    while msj_rec:
    
        peticion = msj_rec.decode()
        orden, argumento = separador_strings(peticion)
        key, info_str = entrada_db(argumento)
        
        if orden == alta or orden == modificacion:
            info = value(info_str)
        
            if info == ():
                respuesta = "Esto no es una peticion valida"
        
            else:
                respuesta = functions_d[orden](key, info)
        
        else:
            if info_str != "":
                respuesta = "Esto no es una peticion valida"
            
            else:
                respuesta = functions_d[orden](key)
       
       
       msj_env = respuesta.encode()

        cl_socket.send(msj_env)

        msj_rec = cl_socket.recv(1024)

    cl_socket.close()

## Inicio de funcionamiento del servidor
db = BaseDeDatos()

functions_d = {
                "alta": alta
                "baja": baja
                "modificacion": modificacion
                "consulta": consulta
                }

srvr_socket = socket()
ip_addr = "localhost"
puerto = 54321
srvr_socket.bind((ip_addr, puerto))


srvr_socket.listen()

while True:
    
    cl_socket, _ = srvr_socket.accept()#bloqueante
    
    hebra = Thread(target = ft_server, args = (cl_socket, functions_d, db))
    hebra.start()


srvr_socket.close()


