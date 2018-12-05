import socket
import sys
import select

# Creation of two sockets
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Sockets created'
except socket.error, msg :
    print 'Failed to create sockets. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
# Bind sockets to addresses: *:8888 for socket s, *:9999 for socket s2
try:
    s.bind(('', 8888))
    s2.bind(('', 9999))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Sockets bind complete'

while 1:
    
   # Await a read event
    rlist, wlist, elist = select.select( [s, s2], [], [], 5 )
    
      # Test for timeout
    if [rlist, wlist, elist] == [ [], [], [] ]:
        print "Han pasado 5 seg sin recibir nada por ningun socket.\n"
    else:
    # Loop through each socket in rlist, read and print the available data
        for sock in rlist:  
            data, addr = sock.recvfrom( 1024 )
            print 'recibido en mi socket ' + str(sock.getsockname()) + ' desde el origen ' + addr[0] + ':' + str(addr[1]) + ': ' + data
            reply = data
            sock.sendto(reply , addr)
     
s.close()
s2.close()
