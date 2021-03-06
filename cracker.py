#!/usr/bin/python

#-----------------------------------#
#		Projet Python3 3I SI		#
#		Groupe : FONTANA - ZOBEC 	#
#-----------------------------------#

#Le but de ce projet est de créer un bruteforceur de hash MD5 et de les tester sur un serveur distant.
#Ce fichier a juste comme but de créer un fichier de hash, une "rainbow-Table"

#Gestion des imports
from itertools import product
from optparse import OptionParser
import optparse
import socket
import sys
import getpass
import hashlib


def try_passwords_on_servers(ip_server,port_server,dico_passwd, test_hash):
	#on ouvre le fichier dictionnaire
	_file = open(dico_passwd,'r')
	sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
	# connexion au serveur, bloc surveillé, et gestion de l'exception
	    sock.connect((ip_server,port_server))

	except socket.error:
	  print("la connexion a échoué.......")
	  sys.exit()

	print(">>> Connexion établie avec le serveur...")
	# Envoi et réception de messages
	msgServer=sock.recv(1024) # taille par défaut

	print(">>> S :", msgServer.decode())
	msgClient = input(">>> Tapez votre login :")
	sock.send(msgClient.encode())
	msgServer = sock.recv(1024)
	print(msgServer.decode())

	#Ensuite on a la boucle de connexion habituelle
	test = True

	while test:
		if msgServer==b'FIN':
			break
		else:
			password = _file.readline()
			password = password.rstrip('\n')
			msgClient = password
			msgClient = msgClient.encode()
			sock.send(msgClient)
			print(">>> Password envoyé")
			msgServer=sock.recv(1024)
			msgServer = msgServer.decode()
			if msgServer ==  "True":
				print(">>> Vous avez trouvé le bon password :")
				print(password)
				sock.send(b'__WAIT__')
				test = False
				break
			#on encode le tout en binaire 
		    
	#Fin while (1) connexion
	print (">>> Connexion interrompue proprement par le serveur")
	#on ferme proprement le socket
	sock.close()
	#on ferme ici proprement le fichier
	_file.close()


#on va demander au client la range qu'il veut taper, s'il veut faire que des minuscules ou pas, etc...
def menu():
	print("-_-_-_-_-_-Bienvenue dans le bruteforceur de hash-_-_-_-_-_-")
	print(">>> Tapez 1 pour : minuscules seulement")
	print(">>> Tapez 2 pour : MAJUSCULES seulement")
	print(">>> Tapez 3 pour : ch1ffr35 seulement")
	print(">>> Tapez 4 pour : minuscules + MAJUSCULES")
	print(">>> Tapez 5 pour : minuscules + MAJUSCULES + ch1ffr35 ")
	print(">>> Tapez 6 pour : minuscules + MAJUSCULES + ch1ffr35 + c@ractères spéci@ux")
	test_user = input("")
	if test_user == "1":
		return "abcdefghijklmnopqrstuvwxyz"
	if test_user == "2":
		return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if test_user == "3":
		return "0123456789"
	if test_user == "4":
		return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if test_user == "5":
		return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	if test_user == "6":
		return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#=!+-_ /:|"
#fin de la fonction menu

#Creation de la fonction itérative qui va envoyer les résultats de l'itération dans un fichier
def iteration_mdp(destination,chars):
	_file = open(destination,"wb")
	print(">>> Renseigner la range voulue au format chiffre;chiffre")
	_range = input("")
	_range = _range.split(";")
	for length in range(int(_range[0]), int(_range[1])+1):
		#intégrer ici le multi-threading?? 
	    list_new_mdp = product(chars, repeat=length)
	    for new_mdp in list_new_mdp:
	        _file.write(bytes((''.join(new_mdp)),'UTF-8'))
	        _file.write(bytes(("\n"),'UTF-8'))
	#On ferme proprement les fichier
	_file.close()

#Fin de la fonction iteration_mdp(destination):

#début du main
if __name__ == "__main__":
	
	dest_file = ""
	dico = ""
	ip_server = ""
	port_server = ""
	test_hash = False

	#parser d'options
	parser = optparse.OptionParser()

	#gestion du file
	parser.add_option("-f", "--file", dest = 'dictionnaire', help= "Choix d'un dictionnaire", metavar = "FILE", default = False)
	parser.add_option("-s", "--server", dest = 'HOST', help = "Choix du serveur à attaquer", metavar = "SERVER", default = False)
	parser.add_option("-w", "--write", dest = 'destination_file', help = "Output du bruteforce", metavar = "FILE", default = False)
	parser.add_option("-p", "--port", dest = 'port', help = "Choix du port", metavar = "PORT", default = False)
	parser.add_option("-H", "--hash", dest = 'hash', help = "Mot de passe en MD5", metavar = "HASH", default = False)

	options,args = parser.parse_args()

	if options.destination_file != False:
		dest_file = options.destination_file
	if options.dictionnaire != False:
		dico = options.dictionnaire
	if options.HOST != False :
		ip_server = options.HOST
	if options.port != False:
		port_server = int(options.port)
	if options.hash != False:
		test_hash = True


	#on va maintenant tester chaque option qu'on a reçu et utiliser les fonctions en conséquence 
	if  dest_file!= "":
		charset = menu() #Obtention du choix de l'utilisateur et donc du charset en conséquence
		print(charset)
		iteration_mdp(dest_file,charset, test_hash)

	if dico != "":
		if ip_server != "":
			if port_server != "":
				try_passwords_on_servers(ip_server,port_server,dico)
			else:
				print(">>> Merci de renseigner un port !")
				exit(1)
		else:
			print(">>> Une IP est nécessaire pour contacter le serveur !")
	else:
		print(">>> Il manque un dictionnaire !")



#Fin du main