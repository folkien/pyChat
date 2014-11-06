#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, datetime, glob, time, sys, platform
from threading import Thread


class colors:
    RED 	= '\033[91m'
    GREEN 	= '\033[92m'
    YELLOW 	= '\033[93m'
    BLUE 	= '\033[94m'
    MAGNETA = '\033[95m'
    CYAN	= '\033[96m'
    WHITE	= '\033[97m'
    ENDC 	= '\033[0m'

session_root = "./session/"

if platform.system() != "Linux":
		username = os.getlogin()
		filename = "session@" + username
else:
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
	users = glob.glob(session_root + "/session@*");
	for user in users:
			if user[18:] != username:
				writefile(user, data)

def is_command(data):
	if (len(data)!=0) and (data[0] == '/'):
			return 1
	else:
			return 0

def execute_command(data):
	return 0

class cReadingProcess:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global actual_time
        while self._running:
			time.sleep(1)
			if actual_time < modification_date(session_root + filename):
				text = readfile(session_root + filename)
				cleanfile(session_root + filename)
				actual_time = datetime.datetime.now()
				sys.stdout.write(text)

###################################################

#pytanie o nazwe uzytkownika, jezeli taki user istnieje to ponownie pytamy
sessionExists = os.path.exists(session_root + filename)
while sessionExists:
    #To znaczy ze mamy juz uzytkownika o takiej nazwie.
	username = raw_input("Ops! Ktoś już ma taki login, musisz go zmienić na inny!\nPodaj swoj nowy login:") 
	filename = "session@" + username
	sessionExists = os.path.exists(session_root + filename)

#tworzenie nowego pliku sesji
cleanfile(session_root + filename)

#aktualny timestamp
actual_time = datetime.datetime.now()

#wysylam informacje do innych uzytkownikow o zalogowaniu
send("Użytkownik " + username + " zalogował się.\n")
print colors.GREEN + "Zalogowałeś się do czatu jako " + username + ". Miłego czatowania! Aby zakończyć działanie programu wpisz /quit." + colors.ENDC

#teraz bedziemy cyklicznie czytac czy plik zostal zmodyfikowany
inputtext = ""
ReadingProcess = cReadingProcess()
threadReadingProcess = Thread(target=ReadingProcess.run)
threadReadingProcess.start()
while inputtext != "/quit":
	# proces rodzica
	inputtext = raw_input()
	if is_command(inputtext):
			execute_command(inputtext[1:])
	else:
			send("<" + colors.MAGNETA + username + colors.ENDC + ">" + colors.YELLOW + inputtext + colors.ENDC + "\n")

#zamykam watek czytajacy
ReadingProcess.terminate()
threadReadingProcess.join()

#wysylam informacje o wylogowaniu użytkownika
send("Użytkownik " + username + " opuścił czat.\n")

#usuwam moj plik sesji
os.remove(session_root + filename)

