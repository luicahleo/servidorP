import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#conectar con el servidor
s.connect(('127.0.0.1',5000))

print 'socket conectado'

#funcion para encapsular el mensaje

def encapsula(mensaje):
    tam = len(mensaje)
    apdu = '{:0>6n}'.format(tam) + ':' + mensaje
    return apdu

#llamada a la funcion antes de enviar el mensaje 1
msg1 = 'h'
apdu = encapsula(msg1)

s.sendall(apdu)
print 'enviado =' + apdu

#llamada a la funcion antes de enviar el mensaje 2
msg2 = 'a'
apdu2 = encapsula(msg2)
s.sendall(apdu2)

print 'enviado =' + apdu2

s.close()
