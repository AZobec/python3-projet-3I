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

login = ""

TAILLE_BUFFER = 1024

list_passwords = {"admin":("admin"),"az":("aa")}

def remplissage(login, password, connexion):
        list_passwords[login]= password 
        item= list_passwords[login]
        msgServer=">>> Vous avez inséré la ligne suivante:Login :%s / Password: %s " %(login,password)
        msgServer=msgServer.encode()
        print(">>> Envoi vers le client de la réponse de remplissage")
        connexion.send(msgServer)         
        
def consultation(login, connexion):
        if login in list_passwords : # le prenom est-il répertorié ?
            item = list_passwords[login] # consultation proprement dite
            msgServer=">>> Le login : %s est répertoriée \nLogin: %s / Password: %s" %(login,login,item)
        else:
            msgServer=">>> *** Login inconnu ! ***"
              
        #on lui envoie le message
        msgServer=msgServer.encode()
        print(">>> Envoi vers le client de la consultation")
        connexion.send(msgServer)             
 
def modification(login, new_password, connexion):
        if login in list_passwords :# le prénom est-il répertorié?
            list_passwords[login]=new_password
            msgServer=">>> Vous avez bien modifié le password de %s. Le nouveau password est : %s" %(login,new_password)
        else:
            msgServer=">>> *** Login inconnu ! ***"
            #On envoie le message
        msgServer=msgServer.encode()
        print(">>> Envoie vers le client le résultat de la modification")
        connexion.send(msgServer)

def administration_liste(connexion):
	while 1 :
		msgClient = connexion.recv(TAILLE_BUFFER)
		msgClient = msgClient.decode()
		listMessage=msgClient.split(";")
		if msgClient == "FIN":
			break
		if listMessage[0] == "0" :
			remplissage(listMessage[1], listMessage[2], connexion)
		if listMessage[0] == "1" :
			consultation(listMessage[1], connexion)
		if listMessage[0] == "2" :
			modification(listMessage[1], listMessage[2], connexion)


def compare_passwords(password_client,login_connexion):
	
	item = list_passwords[login_connexion]
	pwd_server = item
	#comparaison = "comparaison de : "+pwd_server+" avec : "+password_client
	#print (comparaison)
	if pwd_server.encode() == password_client:	
		print("MATCHING")
		return "True"
	else :
		print("FALSE")
		return "False"

if __name__ == "__main__":
	#Sockets et connexions
	HOST='127.0.0.1'
	PORT=2020


	testMessageClient=""

	#Création d'une socket avec la famille IP + TCP
	MySocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#Liaison Socket avec adresse+PORT
	MySocket.bind((HOST, PORT))

	while True:
		#Boucle de traitement tant qu'il y a des clients connectés
		print("S > Serveur prêt, en attente d'un client")

		#ecoute d'une connexion et une seule
		MySocket.listen(1)

		#établissement de la connexion
		connexion,addresse=MySocket.accept()
		print("S > Connexion client réussie, adresse IP %s, port %s \n" %(HOST,PORT))

		# dialogue avec le client, envoi de message
		connexion.send(b'hello client/ SERVEUR IS UP\n>>> Merci de donner un login')
		print(">>> Vous êtes sur le serveur, celui-ci est UP")
		msgClient = connexion.recv(TAILLE_BUFFER)
		login = msgClient.decode()
		msgServer = ">>> Vous êtes connecté avec le login : "+ login+", Merci de rentrer votre password"
		connexion.send(msgServer.encode())
		

		# boucle d'échange avec le client
		while 1 :
			# réception de message du client
			# réception de 1024 caractères
			msgClient=connexion.recv(TAILLE_BUFFER)
			if msgClient.decode()=="__FIN__" :
				break
			elif msgClient.decode()=="__WAIT__": 
				break
			elif msgClient.decode()== "__admin_server__":
				msgServer = (">>> Vous êtes connecté en mode administration de la base")
				msgServer = msgServer.encode()
				connexion.send(msgServer)
				administration_liste(connexion)
				break
			else:
				#intégrer fonction de comparaison avec testMessageClient qui retourne un msgServer
				msgServer = compare_passwords(msgClient,login)
				msgServer = msgServer.encode()
				print(">>> Envoi de la réponse vers le client")
				connexion.send(msgServer)

		# fermeture de la connexion
		connexion.send(b"FIN")
		print(">>> connexion interompue par le client!!!!")

		connexion.close()
		
	MySocket.close()