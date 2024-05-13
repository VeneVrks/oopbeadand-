from abc import ABC, abstractmethod
import os
import time
import re


class Szoba(ABC):
    ar = 0
    szobaszam = 0

class EgyagyasSzoba(Szoba):
    ar = 1500
    agyakSzama = 1

class KetagyasSzoba(Szoba):
    ar = 3000
    agyakSzama = 2

class Szalloda:
    nev = ""
    szobak = []

    def __init__(self, nev, szobak):
        self.nev = nev
        self.szobak = szobak

class Foglalas:
    nev = ""
    szobaszam = 0
    bejelentkezes = ""
    kijelentkezes = ""

    def __init__(self, nev, szobaszam, bejelent, kijelent):
        if not Szalloda.szobak[szobaszam]:
            return False

        self.nev = nev
        self.szobaszam = szobaszam
        self.bejelentkezes = bejelent
        self.kijelentkezes = kijelent

        return Szalloda.szobak[szobaszam].ar
    



szalloda = Szalloda("Teszt Szálloda", [])



foglalasok = []
def foglalasLemondas(szobaszam):
    for i in range(1, len(foglalasok)):
        foglalas = foglalasok[i]

        if foglalas and foglalas.szobaszam == szobaszam:
            foglalasok.pop(i)

            return True

    return False

def foglalasokListazasa():
    for foglalas in foglalasok:
        print(foglalas.szobaszam)




panels = ['foglalás', 'lemondás', 'listázás']
def clearPanel():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def getInput(text, numberOnly):
    value =""
    while value == "" and (numberOnly and not re.match(r"^[0-9]+$", value)):
        value = input(text)

    return value

panel = 0
def drawPanel():
    clearPanel()

    if panel == 0:
        for i in range(0, len(panels)):
            name = panels[i]
            if not name:
                continue

            print(f'{name} {i}')

        
        value = getInput('Válassz menü-t: ', True)

    else:
        print("")


def Main():
    drawPanel()






Main()