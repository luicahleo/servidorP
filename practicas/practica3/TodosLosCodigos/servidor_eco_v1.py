import socket
import sys

HOST = ''   # Symbolic name meaning all interfaces (i.e. 0.0.0.0)
PORT = 44444 # Arbitrary non-privileged port
 
# Datagram (udp) socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
# Bind socket to local host and port
s.bind((HOST, PORT))
print "Soy el servidor. Estoy escuchando en el puerto",PORT     
#now the serving loop. I reply to each message received.
while 1:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
     
    if  data=='.': 
        break
 
    reply =  data
     
    s.sendto(reply , addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
     
s.close()
