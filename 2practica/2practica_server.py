import basedatos
from socket import socket
from threading import Thread


### Funcion para registrar la entrada del cliente ###
# Devuelve las dos partes de la entrada seàradas
def separador_strings(msg:str):
    
    for i in range(len(msg)):
        
        if msg[i] == ' ':
            return msg[:i], msg[i+1:]
    
    return msg, ""
#####################################################
# Devuelve 2 strings, el primero es la key y el segundo el value que vamos a introducir en la db
def entrada_db(info:str):
    for i in range(len(info)):
        if info[i] == ":":
            return info[:i], info[i+1:]
    return info, ""

# Funcion que parsea el futuro value de la base de datos. Devuelve la tupla vacia si encuentra
# un error
def value(msg:str):
    n = len(msg)
    if n != 0 and msg[0] == '(' and msg[n-1] == ')':
        text = msg[1:n-1]
        l = text.split(',')
        try:
            l[0] = int(l[0])
            tuple(l)
            return tuple(l)
        except ValueError:#Si l[0] no es un entero
            return tuple()
    else:
        return tuple()##Input no valido
    
### Funciones de soporte para el servidor ###
def alta(db:basedatos.BaseDeDatos, nombre:str, info:tuple):
    return db.alta(nombre, info)

def baja(db:basedatos.BaseDeDatos, nombre:str):
    return db.baja(nombre)

def modificacion(db:basedatos.BaseDeDatos, nombre:str, info:tuple):
    return db.modificacion(nombre, info)

def consulta(db:basedatos.BaseDeDatos, nombre:str):
    return db.consulta(nombre)
############################################

## Funcion objetivo para las hebras
def ft_server(cl_socket:socket, functions_d:callable, db:basedatos.BaseDeDatos):
    msj_rec = cl_socket.recv(1024)
    while msj_rec:
    
        peticion = msj_rec.decode()
        orden, argumento = separador_strings(peticion) # Separamos entre orden y la key:value
        key, info_str = entrada_db(argumento) # Separamos entre la key y el value
        
        if orden == "alta" or orden == "modificacion":# Si la orden necesita un value para ejecutarse
            info = value(info_str)
            if info == tuple():# Comprobamos si el cliente ha proporcionado value
                respuesta = "Esto no es una peticion valida"
        
            else:
                respuesta = functions_d[orden](db, key, info)
        
        else:# Si la orden no necesita el value para ejecutarse
            if info_str != "":
                respuesta = "Esto no es una peticion valida"
            
            else:
                respuesta = functions_d[orden](db, key)
       
       
        msj_env = respuesta.encode()

        cl_socket.send(msj_env)

        msj_rec = cl_socket.recv(1024)

    cl_socket.close()

## Inicio de funcionamiento del servidor
db = basedatos.BaseDeDatos()

functions_d = {
                "alta": alta,
                "baja": baja,
                "modificacion": modificacion,
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


