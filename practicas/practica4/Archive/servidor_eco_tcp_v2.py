import socket
import sys
import select
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete, port' + str(PORT)
 
s.listen(10)
print 'Socket now listening'

descriptors = [s]

#now keep talking with the client
while 1:
    #list of sockets to watch for read events
    (sread, swrite, sexc) = select.select( descriptors, [], [] )

    for sock in sread:
        if sock == s:   #socket s is the listening socket, so this is a connect request
             conn, addr = s.accept()
             print 'Connected to ' + addr[0] + ':' + str(addr[1])
             descriptors.append(conn)   #sock object added to the list to watch
        else:
            data = sock.recv(100)
            if data =='':
                host,port = sock.getpeername()
                msg = 'client left ' + str(host) + ':' + str(port)
                print msg
                sock.close()
                descriptors.remove(sock)
            else:
                host,port = sock.getpeername()
                msg = 'client ' + str(host) + ':' + str(port) + 'data: ' + str(data)
                print msg
                reply = data
                sock.sendall(data)

s.close()
