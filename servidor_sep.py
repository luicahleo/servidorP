

#Luis Rolando Cahuana Leon luicahleo

import socket
import sys
import select
import hashlib

TIMEOUT = 10.0


if len(sys.argv) != 3 :
	print("Error. Use: server port error ");
	sys.exit();

#guardamos el puerto
puerto = sys.argv[1];

#guardamos el modo
modo = sys.argv[2];

localHost = "127.0.0.1";
# Creation of two sockets
try :
    servidorUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

except socket.error, msg :
    print 'Failed to create socke. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
# Bind socket to address: *:8888
try:
    servidorUDP.bind((localHost, int(puerto)))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()


# set timeout for socket s blocking operations
#servidorUDP.settimeout(TIMEOUT)
print "Servidor a la escucha en puerto: " + puerto;


################################################################
####Creamos socket TCP#########################################
###############################################################

try:
	servidorTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        servidorTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1);
except socket.error:
        print "Error al crear socket TCP";
        sys.exit();
#conectamos el socket con el cliente
try:
        servidorTCP.bind((localHost,int(puerto)));
except socket.error, msg:
        print "Bind failed. Error code : " + str(msg[0]) + " Message " + msg[1];
        sys.exit();
#print "DEBUG::::::::::entra";	
#vamos a escuchar a 3 clientes
servidorTCP.listen(3);
#print "DEBUG::::::::::entra";
#conn,addr = servidorTCP.accept();
#print "DEBUG::::::::::entra";
###################################################################










correctoUDP = False;
correctoTCP = False;
flag_transfer_done = False;
contador  = 0;

flag_ficheroTXT_largo = False;
#print "DEBUG::::::::::entra";

try:
    while 1:
    
       
        data, addr = servidorUDP.recvfrom(1024)
        print 'recibido desde ' + addr[0] + ':' + str(addr[1]) + ': ' + data
        
	data_aux = data.split(" ");

       	data_len = len(data_aux);

	##############################################################
	# si el tamano es dos, quiere decir que es fichero.txt #numero
	#############################################################
	
	if flag_ficheroTXT_largo == False:
		if data_len == 2:
			print "DEBUG::::::::::entra";
			flag_ficheroTXT_largo = True;
			if data_aux[0] == "fichero.txt":
				print "DEBUG::::::::::entra a flag_fichero";
				print "nombre de fichero incorrecto";
        			#sys.exit();
        			tam_datos = int(data_aux[1]);
				print "REQ received, sending " + data + "from : (" + "\'" + addr[0] + "\'"+" , " + str(addr[1])  + ")";
				print "abriendo puerto : " + puerto;
				#si todo pasa bien, enviamos ok
				servidorUDP.sendto("ok", addr);
        
        ##############################################################
        ##############################################################
        	
        #para la parte del TCP , el socket ya esta creado
        if flag_ficheroTXT_largo == True:
        	print "DEBUG::::::::::entra TCP";
        	
        	#entramos a bucle para recibir el contenido del fichero que envia cliente
        	if flag_transfer_done == False:
        		conn,addr = servidorTCP.accept();
        		dataTCP = conn.recv(1024);

        		#pregunta si los datos llegados son vacios
        		if dataTCP == '':
        			correctoTCP = True;
        			print "El fichero esta vacio";
        			break;
        		else:
        			#enviamos mensaje transfer done 
        	       		conn.sendall('transfer done');
        			conn.close();
        			
        			#hacemos el md5
        			h = hashlib.md5();
				h.update(dataTCP);
				checksum = h.hexdigest();
				
				print "Calculado md5sum =  " + str(checksum);
				
				correctoTCP == True;
			        flag_transfer_done = True;
				#print "debug md5::::" + checksum;
        	
		if flag_transfer_done:
		       	data, addr = servidorUDP.recvfrom(1024)
		       	print "Recibido md5sum = " + str(data);
        		#print 'recibido desde ' + addr[0] + ':' + str(addr[1]) + ': ' + data
			#print data;
			#print checksum;
	
			
			if checksum == data:
				print "copia de fichero correcta";
				servidorUDP.sendto("md5sum ok", addr);
				#cuando ya todo este terminado, volvemos a poner los flags en False
				flag_ficheroTXT_largo = False;
				flag_transfer_done = False
        			

        
        
        #servidorUDP.sendto(reply , addr)
except socket.timeout,t:
    print '** Exception : socket' + str(s.getsockname()) + str(t[0]) + '  after ' + str(TIMEOUT) + ' seg.'
    

    
    
    servidorUDP.close()
    sys.exit()

servidorUDP.close()

