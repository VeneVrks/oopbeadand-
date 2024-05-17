from abc import ABC, abstractmethod
import os
import time
import re
import random
from datetime import datetime, date, timedelta

class Szoba(ABC):
    ar = 0
    szobaszam = 0

    def __init__(self, szobaszam):
        self.szobaszam = szobaszam

class EgyagyasSzoba(Szoba):
    ar = 1500
    agyakSzama = 1

class KetagyasSzoba(Szoba):
    ar = 3000
    agyakSzama = 2

class Szalloda:
    nev = ""
    szobak = []

    def __init__(self, nev):
        szobak = []
        for i in range(0, random.randint(3, 10)):
            egyagyas = random.randint(0, 1) == 1
            
            szoba = False
            if egyagyas:
                szoba = EgyagyasSzoba(i)
            else:
                szoba = KetagyasSzoba(i)
            
            szobak.append(szoba)

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
    



szalloda = Szalloda("Teszt Szálloda")



foglalasok = []
def foglalasLemondas(foglalasID):
    if not foglalasID:
        return False
    
    foglalasok.pop(int(foglalasID))
    return True

def foglalasHozaadasa(nev, szobaszam, datum):
    if not nev or not szobaszam or not datum:
        return False
    
    adat = {
        'nev': nev,
        'szobaszam': szobaszam,
        'datum': datum,
        'ar': szalloda.szobak[szobaszam].ar,
        'agyakSzama': szalloda.szobak[szobaszam].agyakSzama,
    }
    foglalasok.append(adat)
    
    return szalloda.szobak[szobaszam].ar

def foglalasokListazasa(showID):
    if len(foglalasok) == 0:
        print('Nincs jelenleg egy foglalás sem!')
        return

    foglalasID = 1
    for foglalas in foglalasok:
        if showID:
            print(f'foglalásID: {foglalasID}, szobaszám: {foglalas['szobaszam']}, foglalva: {foglalas['datum']}, név: {foglalas['nev']}, ágyak száma: {foglalas['agyakSzama']}, ár: {foglalas['ar']}Ft')
        else:
            print(f'szobaszám: {foglalas['szobaszam']}, foglalva: {foglalas['datum']}, név: {foglalas['nev']}, ágyak száma: {foglalas['agyakSzama']}, ár: {foglalas['ar']}Ft')

        foglalasID += 1

foglalasHozaadasa('Kis Pista', 1, '2025-10-10')
foglalasHozaadasa('Kis Pista', 1, '2025-10-13')
foglalasHozaadasa('Kis Pista', 2, '2025-10-10')





panels = ['foglalás', 'lemondás', 'listázás', 'kilépés']
def clearPanel():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def getInput(text, numberOnly):
    value =""
    while value == "" or (numberOnly and not re.match(r"^[0-9]+$", value)):
        value = input(text)

    return value

def drawPanel(panel):
    clearPanel()

    if panel == 0: # Főmenü
        print(f"Üdvözöljük a {szalloda.nev} recepciós rendszerébe.")

        text = ""
        for i in range(0, len(panels)):
            name = panels[i]
            if not name:
                continue
            
            text += f'{name}: {i+1} '
        print(text)
        
        panelID = int(getInput('Válassz menü-t: ', True))
        while panelID < 1 or panelID > len(panels):
            panelID = int(getInput('Válassz menü-t: ', True))

        drawPanel(panelID)
    elif panel == 1: # Foglalás
        print("Szobák: ")
        for szoba in szalloda.szobak:
            print(f'  szobaszám: {szoba.szobaszam}, ár: {szoba.ar}Ft, Ágyak száma: {szoba.agyakSzama}')
        
        nev = getInput('Adja meg a nevét: ', False)
        while not re.match(r'[A-Za-z]+ [A-Za-z]+', nev):
            nev = getInput('Adja meg a nevét: ', False)

        szobaszabad = False
        while not szobaszabad:
            szobaszam = int(getInput('Válassz szobaszámot: ', True))
            while szobaszam < 0 or szobaszam > len(szalloda.szobak) - 1:
                szobaszam = int(getInput('Válassz szobaszámot: ', True))

            datum = getInput('Válassz dátumot: ', False)
            while not re.match(r"\b(19\d\d|20\d\d)[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])\b", datum) or datetime.strptime(datum, '%Y-%m-%d').date() < date.today():
                datum = getInput('Válassz dátumot: ', False)

            talalat = False
            for foglalas in foglalasok:
                if foglalas['szobaszam'] == szobaszam:
                    foglaltDatum = datetime.strptime(foglalas['datum'], '%Y-%m-%d').date()
                    bekertDatum = datetime.strptime(datum, '%Y-%m-%d').date()

                    if foglaltDatum == bekertDatum or foglaltDatum + timedelta(days=1) == bekertDatum or bekertDatum - timedelta(days=-1) == foglaltDatum:
                        talalat = True
                        break

            szobaszabad = not talalat

            if not szobaszabad:
                print('Ez a szoba már levan foglalva erre az időpontra!')
                time.sleep(1)

        result = foglalasHozaadasa(nev, szobaszam, datum)
        if result:
            print('Foglalás sikeres!')
            print(f'Szoba ára: {result}Ft')

        time.sleep(2)
        drawPanel(0)
    elif panel == 2: # Lemondás
        foglalasokListazasa(True)
        print('Visszalépéshez irja be a 0-át.')

        foglalasID = int(getInput('Válassz foglalást!: ', True))
        while foglalasID < 0 or foglalasID > len(foglalasok):
            foglalasID = int(getInput('Válassz foglalást!: ', True))

        if foglalasID == 0:
            drawPanel(0)

        foglalasID -= 1
        foglalas = foglalasok[foglalasID]
        print(f'szobaszám: {foglalas['szobaszam']}, foglalva: {foglalas['datum']}, ágyak száma: {foglalas['agyakSzama']}, ár: {foglalas['ar']}Ft')
        
        value = getInput('Biztosan ezt szeretné törölni? (igen, nem) ', False)
        while value != 'igen' and value != 'nem':
            value = getInput('Biztosan ezt szeretné törölni? (igen, nem) ', False)

        if value == 'igen':
            foglalasLemondas(foglalasID)
            drawPanel(0)
        else:
            drawPanel(2)
    elif panel == 3: # Listázás
        foglalasokListazasa(False)
        print('visszalépés: 0')

        value = int(getInput('Válassz menü-t: ', True))
        while value != 0:
            value = int(getInput('Válassz menü-t: ', True))

        panel = value
        drawPanel(panel)
    elif panel == 4: # Kilépés
        print("Viszont látásra!")
        time.sleep(2)
        clearPanel()
        exit()


def Main():
    drawPanel(0)

Main()