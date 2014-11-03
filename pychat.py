#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, datetime

username = os.environ['USER']
filename = "session@" + username

#pytanie o nazwe uzytkownika, jezeli taki user istnieje to ponownie pytamy

if os.path.exists("./session/" + filename):
    #To znaczy ze mamy juz uzytkownika o takiej nazwie.
    print "Ops! Ktoś już ma taki login, musisz go zmienić na inny!"
else:
    #tworzenie nowego pliku sesji
    session = open("./session/" + filename, 'w')
    session.close();

    #aktualny timestamp
    actual_time = datetime.datetime.now()

    #teraz bedziemy cyklicznie czytac czy plik zostal zmodyfikowany
    
#zapamietanie timestampa sesji

#Petla while command != /quit

#jeden watek co kilka sekund sprawdza czy plik zostal zmodyfikowany

#inny watek czeka na input os user'a

