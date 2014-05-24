#!/usr/bin/python

#-----------------------------------#
#		Projet Python3 3I SI		#
#		Groupe : FONTANA - ZOBEC 	#
#-----------------------------------#

#Le but de ce projet est de créer un bruteforceur de hash MD5 et de les tester sur un serveur distant.
#Ce fichier a juste comme but de créer un fichier de hash, une "rainbow-Table" OU de tester les pwd

#Gestion des imports
import socket
import sys
import getpass
import hashlib

TAILLE_BUFFER = 1024

# création d'un socket pour la connexion avec le serveur en local
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
# connexion au serveur, bloc surveillé, et gestion de l'exception
	sock.connect(('127.0.0.1',2020))

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
msgClient = "__admin_server__"
sock.send(msgClient.encode())
#On envoie d'abord le dictionnaire au serveur via une boucle




#Ensuite on a la boucle de connexion habituelle
while 1:
	if msgServer==b'FIN':
		break
	print(">>> Quelle action voulez-vous effectuer?")
	print(">>> CODE 0: Ajout d'une ligne à la base de mdp")
	print(">>> CODE 1: Consultation d'une ligne de la base")
	print(">>> CODE 2: Modification d'une ligne de la base")
	print(">>> CODE Q: Quitter le programme")

	msgClient=input(">>> Choisissez votre action : ")

	#Gestion du menu
	#En cas de demande d'ajout :
	if msgClient=="0":
		print(">>> Tapez maintenant : login;password")
		msgClient=input("")
		#on concatene le message au code pour que le serveur puisse l'interpréer
		msgClient="0;"+msgClient

	#En cas de demande de consultation 
	if msgClient=="1":
		print(">>> Tapez le login de personne à rechercher")
		msgClient=input("")
		msgClient="1;"+msgClient

	#En cas de demande de Modification
	if msgClient=="2":
		print(">>> Tapez maintenant: login;NewPassword")
		msgClient=input("")
		msgClient="2;"+msgClient

	#En cas de quitte
	if msgClient=="q":
		msgClient="FIN"

	msgClient=msgClient.encode()
	print(">>> Envoi vers le serveur")
	sock.send(msgClient)         
	msgServer=sock.recv(1024)
	print(">>> Reception du serveur")
	print(msgServer.decode())

#Fin while (1) connexion
print (">>> Connexion interrompue par le serveur!!!")
sock.close()