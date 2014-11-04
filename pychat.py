#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, datetime, glob, time, sys
from threading import Thread

username = os.environ['USER']
filename = "session@" + username

#funkcje
###################################################
def modification_date(filename):
		    t = os.path.getmtime(filename)
		    return datetime.datetime.fromtimestamp(t)

def writefile(filename,data):
	f = open(filename,'a')
	while f.closed:
		time.sleep(1)
		f = open(filename,'a')
	f.write(data)
	f.close()

def cleanfile(filename):
	f = open(filename,'w')
	while f.closed:
		time.sleep(1)
		f = open(filename,'w')
	f.close()

def readfile(filename):
	f = open(filename,'r')
	while f.closed:
		time.sleep(1)
		f = open(filename,'r')
	data = f.read()
	f.close()
	return data

def send(data):
	global username
	users = glob.glob("./session/session@*");
	for user in users:
			if user[18:] != username:
				writefile(user,data)


class cReadingProcess:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global actual_time
        while self._running:
			time.sleep(3)
			if actual_time < modification_date("./session/" + filename):
				text = readfile("./session/" + filename)
				cleanfile("./session/" + filename)
				actual_time = datetime.datetime.now()
				sys.stdout.write(text)

###################################################

#pytanie o nazwe uzytkownika, jezeli taki user istnieje to ponownie pytamy
sessionExists = os.path.exists("./session/" + filename)
while sessionExists:
    #To znaczy ze mamy juz uzytkownika o takiej nazwie.
	username = raw_input("Ops! Ktoś już ma taki login, musisz go zmienić na inny!\nPodaj swoj nowy login:") 
	filename = "session@" + username
	sessionExists = os.path.exists("./session/" + filename)

#tworzenie nowego pliku sesji
cleanfile("./session/" + filename)

#aktualny timestamp
actual_time = datetime.datetime.now()

#wysylam informacje do innych uzytkownikow o zalogowaniu
send("Użytkownik " + username + " zalogował się.\n")

#teraz bedziemy cyklicznie czytac czy plik zostal zmodyfikowany
inputtext = ""
ReadingProcess = cReadingProcess()
threadReadingProcess = Thread(target=ReadingProcess.run)
threadReadingProcess.start()
while inputtext != "quit":
	# proces rodzica
	inputtext = raw_input()
	send("<" + username + ">" +inputtext+ "\n")

#zamykam watek czytajacy
ReadingProcess.terminate()
threadReadingProcess.join()

#usuwam moj plik sesji
os.remove("./session/" + filename)

