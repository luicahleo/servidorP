import socket  # for sockets
import sys  # for exit
import os #para peso de fichero




flagRegistro = False
flagReplica = False

if len(sys.argv) == 1:
    print "tiene que tener al menos 1 parametro"
    sys.exit();

elif len(sys.argv) == 2:
    host = sys.argv[1]
    print "solo registro"
    flagRegistro = True
    
elif len(sys.argv) == 3:
    host = sys.argv[1]
    fichero = sys.argv[2]
    print fichero
    print "replica"
    
    #tratamos el fichero, para enviarlo como <nombreFichero> <numero de bytes>
    pesoFichero = os.path.getsize('./mifichero.txt')
    
    flagReplica = True
elif len(sys.argv) > 3:
    print "Error. Uso: cliente IP [fichero]"
    sys.exit();

puertoParaTCP = 45000
puertoDestino = 55000
lista = "LISTA"
clientes = ""
hostPortThis = host+","+str(puertoParaTCP)
while (1):
    
    if flagRegistro:
        
        # creamos sockek UDP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(str(puertoParaTCP), (host, puertoDestino))
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]
        
        if reply == 'ok':
            flagRegistro = False  
            
            sTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sTCP.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sTCP.bind((host, puertoParaTCP))
            except socket.error , msg:
                print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                sys.exit()
            
            sTCP.listen(1)
            print 'Socket now listening'
            
            #wait for connection and return a new socket and the remote address
            conn, addr = sTCP.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            
            data = conn.recv(1024)

            recibido = True
            while recibido:
                
                if data != "":
                    conn.sendall("ok")
                    recibido = False
                print "esperando nombre fichero y peso"

            recibido = True
            while recibido:
                
                data = conn.recv(1024)
                if data == '':
                    recibido = False
                    conn.sendall("transfer done")
                print "recibiendo fichero"

            conn.close()
            print 'Disconnected ' + addr[0] + ':' + str(addr[1])
            sTCP.close()
    if flagReplica:
        
        # creamos sockek UDP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(lista, (host, puertoDestino))
        d = s.recvfrom(1024)
        reply = d[0]
        addr = d[1]
        
        #procesamos la cadena para tener 
        #ordenado la lista de clientes conectados
        
        cadena = reply.split(";")
        
        
        #preguntamos si nuestro host y puerto estan en la lista
        if hostPortThis in cadena:
            cadena.remove(hostPortThis)
            totalClientes = len(cadena)
            
            for x in cadena:
                print x
                hostPortList = x.split(",")
                hostList = hostPortList[0]
                portList = hostPortList[1]
                
                try:
                    sVariable = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                except socket.error:
                    print 'Failed to create socket'
                    sys.exit()
                    print 'Socket Created'
                
                #Connect to remote server
                sVariable.connect((hostList , portList))
                print 'Socket Connected to ' + str(hostList) + "Port: " + str(portList)
                try :
                    #Set the whole string
                    sVariable.sendall(fichero + " " + str(pesoFichero))
                except socket.error:
                    #Send failed
                    print 'Send failed'
                    sys.exit()
                print 'Message send successfully'
                
                reply = sVariable.recv(4096)
                print "respuesta del cliente: "+reply
                
                
     
        else:
            print "primero tiene que registrar este cliente"
        
        while flagReplica:
            continue



    break
s.close()   
sys.exit();

