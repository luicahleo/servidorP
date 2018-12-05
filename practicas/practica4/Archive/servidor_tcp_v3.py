import socket
import sys
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket de escucha en la direccion *:5000
s.bind(('',5000))

s.listen(10)
conn, addr = s.accept()

#funcion para desencapsular y leer el mensaje
def readmsg(conn):
    data = conn.recv(8)  #recibo los 8 primeros bytes
    c = data.split(':') # desencapsulo c[0] - bytes a leer en el mensaje
    tamano = int(c[0])
    msg = c[1]   # c[1] si hubiese un mensaje de un byte ya hemos terminado.
    pending = tamano - len(c[1])  # bytes pendientes de leer

    while(pending > 0):
        data = conn.recv(pending)
        msg = msg + data
        pending = pending - len(data)
    return msg

time.sleep(2)

mensaje1 = readmsg(conn)
print mensaje1

mensaje2 = readmsg(conn)
print mensaje2

s.close()
