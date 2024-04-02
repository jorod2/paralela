from socket import socket

### Vamos a hacer entradas en una base de datos. El servidor acepta comandos del tipo:
#       orden key:info
# orden es una palabra de la lista de funciones
# key es un string con el que accederemos a la informacion
# info tiene que ser una tupla con 3 entradas: (Edad:int,Ciudad:str,telefono:str)



def primera_palabra(msg:str):
    resultado = ""
    
    for i in range(len(msg)):
        
        if msg[i] == ' ':
            return resultado
        
        else:
            resultado += msg[i]
    
    return resultado


sckt = socket()
srvr_ip = 'localhost'
srvr_puerto = 54321

sckt.connect((srvr_ip, srvr_puerto))

functions_l = ["alta", "baja", "modificacion", "consulta"]

flag = True
while flag:
    
    
    orden = input("Escribe una orden: ")
    comando = primera_palabra(orden)
    
    if comando == "salir":

        flag = False
    
    elif comando in functions_l:
        
        msj_env = orden.encode()
        sckt.send(msj_env)
        msj_rec = sckt.recv(1024)
        respuesta = msj_rec.decode()
        print(f"Segun el servidor, {orden} es {respuesta}", flush = True)
            

    elif comando == "help":
        print("Los comandos disponibles son:", flush = True)
        for key in functions_l:
            print(f"{key}", flush = True)
    
    else:
        print("Esto no es una orden valida. Escribe help para"
                "la lista de comandos o \"salir\" para salir del programa", flush = True)

sckt.close()



