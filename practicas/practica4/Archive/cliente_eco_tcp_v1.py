import socket   #for sockets
import sys  #for exit

if len(sys.argv) != 3:
    print 'Usage: python %s <HostName> <PortNumber>' % (sys.argv[0])
    sys.exit();

host=sys.argv[1]
port=int(sys.argv[2])

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

s.connect((remote_ip , port))

print 'Socket conectado '

 
while(1) :
    msg = raw_input('Enter message to send : ')
     
    try :
        #Set the whole string
        s.sendall(msg)
         
        # receive data from client (data, addr)
        reply = s.recv(1024)
         
        print 'Server reply : ' + reply
     
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
