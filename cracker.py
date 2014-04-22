#!/usr/bin/python

#-----------------------------------#
#		Projet Python3 3I SI		#
#		Groupe : FONTANA - ZOBEC 	#
#-----------------------------------#

#Le but de ce projet est de créer un bruteforceur de hash MD5 et de les tester sur un serveur distant.
#Ce fichier a juste comme but de créer un fichier de hash, une "rainbow-Table"

#Gestion des imports
from itertools import product

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
	_file_ = open(destination,"wb")
	print(">>> Renseigner la range voulue au format chiffre;chiffre")
	_range_ = input("")
	_range_ = _range_.split(";")
	for length in range(int(_range_[0]), int(_range_[1])+1): 
	    liste_new_mdp = product(chars, repeat=length)
	    for new_mdp in list_new_mdp:
	        _file_.write(bytes((''.join(new_mdp)),'UTF-8'))
	        _file_.write(bytes(("\n"),'UTF-8'))
	#On ferme proprement les fichier
	_file_.close()

#Fin de la fonction iteration_mdp(destination):

#début du main
if __name__ == "__main__":
	
	destination_file = "dictionnaire_iteration.txt"
	charset = menu() #Obtention du choix de l'utilisateur et donc du charset en conséquence
	print(charset)
	iteration_mdp(destination_file,charset)

#Fin du main
	