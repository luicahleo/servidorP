import socket
import sys

TIMEOUT = 5.0
# Creation of two sockets
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socke. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
# Bind socket to address: *:8888
try:
    s.bind(('', 8888))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'

# set timeout for socket s blocking operations
s.settimeout(TIMEOUT)

try:
    while 1:
        data, addr = s.recvfrom(1024)
        print 'recibido desde ' + addr[0] + ':' + str(addr[1]) + ': ' + data
        reply = data
        sock.sendto(reply , addr)
except socket.timeout,t:
    print '** Exception : socket' + str(s.getsockname()) + str(t[0]) + '  after ' + str(TIMEOUT) + ' seg.'
    s.close()
    sys.exit()
s.close()

