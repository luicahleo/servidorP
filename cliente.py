


#Luis Rolando Cahuana Leon luicahleo prueba


import sys
import os
import socket
import hashlib
TIMEOUT3 = 3.0
TIMEOUT10 = 10.0


if len(sys.argv) != 2 :
	print("Error. Uso: Cliente cliente.py");
	sys.exit();

#se guarda el nombre del fichero sea cual sea
nombre_fichero = sys.argv[1];


#verificamos si al menos hay una linea en el fichero de config
try:
	fichero_config = open('./config.txt')
except IOError:
	print('Error: no hay servidores o fichero de configuracion');
	sys.exit();
#se guardan las lineas en dicha variable
lineas_config = fichero_config.readlines();
lineas_config_len = len(open('./config.txt').readlines());


#verificamos que tenga al menos una linea
if lineas_config_len == 0:

	print('Error: no hay servidores o fichero de configuracion')
	sys.exit();

try:
	fichero_config.close();
except IOError:
	print("Error no se ha podido cerrar e fichero config");
	


try:
	fichero_enviar = open(nombre_fichero);
except IOError:
	print("Error. Fichero " + nombre_fichero + " inexistente")
	sys.exit();
tam_fichero = os.path.getsize(nombre_fichero);
#cadena para enviar 
mensajeUDP = nombre_fichero + ' ' + str(tam_fichero);
#contenido del fichero 
contenido = fichero_enviar.read();

try:
	fichero_enviar.close();
except IOError:
	print 'Error. no se ha podido cerrar el fichero ' + nombre_fichero;
	sys.exit();
#####################################################	
#bucle infinito para los servidores
#####################################################
linea = 0;
for i in range(lineas_config_len):
	
	
	flag_error = 0;
	
	servidor = lineas_config[linea];
	
	cadena = lineas_config[linea].split(" ");

		
	ip = cadena[0];

	puerto = int(cadena[1]);


	
	try:
        	clienteUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        except socket.error:
        	flag_error = -1;
        	print 'Eror al crear el socket UDP';
        	sys.exit();
	
	if flag_error == 0:
		#enviamos mensaje si no hay erro al crear el socket UDP
		try:
			clienteUDP.sendto(mensajeUDP, (ip, puerto));
		except socket.error:
			print "No se pudo enviar el mensaje";
			flag_error = 1;
	#esperamo a respuesta por 3 segundos, con el flag_error = 0
	if flag_error == 0:
		clienteUDP.settimeout(TIMEOUT3);
		#definimos el flag_respuestaUDP como string ya que esperamos un string como respuesta del servidor
		cadena_respuestaUDP = '0';
		try:
			res1 = clienteUDP.recvfrom(1024);
			cadena_respuestaUDP = res1[0];
		except socket.timeout,t:
			print "Error. no hay respuesta por parte del servidor " + ip + " en el puerto " + str(puerto);
			clienteUDP.close();
			
		#preuntamos si la respuesta es 'ok'
		if cadena_respuestaUDP == 'ok':
			correcto = 1;

			while correcto:
				#creamos socket TCP
				try:
					clienteTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
				except socket.error:
					print "Error al crear socket TCP";
					sys.exit();
					
				#conectamos el socket con el servidor
				try:
					clienteTCP.connect((ip, puerto));
				except socket.error:
					print "No se pudo conectar con el servidor";
					correcto = 0;
				try:
					clienteTCP.sendall(contenido);
				except socket.error, msg:
					print "Error. no se ha podido enviar el contenido del fichero";
					correcto  = 0;
				#se crea variable para recibir la respuesta de TCP
				cadena_respuestaTCP = '0';
				#establecimiento de tiempo de respuesta de 10 segundos
				clienteTCP.settimeout(TIMEOUT10);
				try:
					cadena_respuestaTCP = clienteTCP.recv(1024);
				except socket.timeout,t:
					print "Error en la transferencia con el servidor " + ip;
					correcto = 0;
				#preuntamos por la respuesta de TCP
				if cadena_respuestaTCP == 'transfer done':

					h = hashlib.md5();
					h.update(contenido);
					checksum = h.hexdigest();
					
					#enviamos el checksum por el UDP inicial
					try:
						clienteUDP.sendto(checksum, (ip, puerto));
					except socket.error:
						print "No se pudo enviar el mensaje con el checksum al servidor";
						correcto = 0;
					#establecemos tiempo de espera de 10 seg para recibir la respuesta
					clienteUDP.settimeout(TIMEOUT10);
					respuesta_checksum = '0';
					
					try: 
						res2 = clienteUDP.recvfrom(1024);
						respuesta_checksum = res2[0];
					except socket.timeout,t:
						print "Error en la copia del fichero en el servidor " + ip + " Finalizado el intento";
						correcto = 0;
					if respuesta_checksum == 'md5sum ok':
						print "Copia de fichero en servidor " + ip + " correcta";
						correcto= 0;
					#si el checksum no coincide
					if respuesta_checksum == 'md5um error':
						print "Error en la copia del fichero en servidor " + ip + ". Se vuelve a intentar ";
	
			##cerramos los sockets que se han abierto
			clienteTCP.close();
			clienteUDP.close();
		if cadena_respuestaUDP == 'no':
			print "Error. El servidor " + ip + " no acepta el fichero";
			clienteUDP.close();
			
	else:
		sys.exit();
		
	linea = linea+1;
sys.exit();










