from datetime import datetime

class Zadanie:
    def __init__(self, tytul, opis, termin):
        self.tytul = tytul
        self.opis = opis
        self.termin = termin
        self.wykonane = False

    def __str__(self):
        status = "Wykonane" if self.wykonane else "Niewykonane"
        return f"Tytuł: {self.tytul}\nOpis: {self.opis}\nTermin wykonania: {self.termin}\nStatus: {status}"
    
class ZadaniePriorytetowe(Zadanie):
    def __init__(self, tytul, opis, termin, priorytet):
        super().__init__(tytul, opis, termin)
        self.priorytet = priorytet

    def __str__(self):
        return super().__str__() + f"\nPriorytet: {self.priorytet}"
    
class ZadanieRegularne(Zadanie):
    def __init__(self, tytul, opis, termin, powtarzalnosc):
        super().__init__(tytul, opis, termin)
        self.powtarzalnosc = powtarzalnosc

    def __str__(self):
        return super().__str__() + f"\nPowtarzalność: {self.powtarzalnosc}"

class ManagerZadan:
    def __init__(self):
        self.zadania = []

    def dodaj_zadanie(self, zadanie):
        self.zadania.append(zadanie)

    def usun_zadanie(self, tytul):
        for zadanie in self.zadania:
            if zadanie.tytul == tytul:
                self.zadania.remove(zadanie)
                return
            
        print("Zadanie o podanym tytule nie istnieje.")

    def oznacz_jako_wykonane(self, tytul):
        for zadanie in self.zadania:
            if zadanie.tytul == tytul:
                zadanie.wykonane = True
                return
            
        print("Zadanie o podanym tytule nie istnieje.")

    def edytuj_zadanie(self, tytul, nowe_dane):
        for zadanie in self.zadania:
            if zadanie.tytul == tytul:
                zadanie.tytul = nowe_dane['tytul']
                zadanie.opis = nowe_dane['opis']
                zadanie.termin = nowe_dane['termin']

                if 'priorytet' in nowe_dane:
                    zadanie.priorytet = nowe_dane['priorytet']
                if 'powtarzalnosc' in nowe_dane:
                    zadanie.powtarzalnosc - nowe_dane['powtarzalnosc']
                return
            
        print("Zadanie o podanym tytule nie istnieje.")

    def sortuj(self):
        self.zadania.sort(key=lambda x: datetime.strptime(x.termin, "%Y-%m-%d"))

    def __contatins__(self, tytul):
        for zadanie in self.zadania:
            if zadanie.tytul == tytul:
                return True
            
        return False
