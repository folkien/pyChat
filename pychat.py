#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, datetime, glob


#funkcje
###################################################
def writefile(filename,data):
	f = open(filename,'a')
	while f.closed:
		f = open(filename,'a')
	f.write(data)
	f.close()

def cleanfile(filename):
	f = open(filename,'w')
	while f.closed:
		f = open(filename,'w')
	f.close()

def readfile(filename):
	f = open(filename,'r')
	while f.closed:
		f = open(filename,'r')
	data = f.read()
	f.close()
	return data

def send(data):
	users = glob.glob("./session/session@*");
	for user in users:
			writefile(user,data)
###################################################
username = os.environ['USER']
filename = "session@" + username

#pytanie o nazwe uzytkownika, jezeli taki user istnieje to ponownie pytamy
sessionExists = os.path.exists("./session/" + filename)
while sessionExists:
    #To znaczy ze mamy juz uzytkownika o takiej nazwie.
	print "Ops! Ktoś już ma taki login, musisz go zmienić na inny!\n"
	username = raw_input("Podaj swoj nowy login:") 
	filename = "session@" + username
	sessionExists = os.path.exists("./session/" + filename)

#tworzenie nowego pliku sesji
cleanfile("./session/" + filename)

#aktualny timestamp
actual_time = datetime.datetime.now()

#wysylam informacje do innych uzytkownikow o zalogowaniu
send("Użytkownik " + username + " zalogował się.\n")

#teraz bedziemy cyklicznie czytac czy plik zostal zmodyfikowany
    
#zapamietanie timestampa sesji

#Petla while command != /quit

#jeden watek co kilka sekund sprawdza czy plik zostal zmodyfikowany

#inny watek czeka na input os user'a

