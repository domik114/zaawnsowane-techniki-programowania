from datetime import datetime
from time import time

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
    """ Klasa Manager Zadan """
    def __init__(self):
        self.zadania = []
        self.start = ''
        self.koniec = ''

    def dodaj_zadanie(self, zadanie):
        """ 
        Funkcja dodaj_zadanie.
        Funkcja dodaje zadania do pliku o nazwie zadania.txt.
        :param zadanie: obiekt zadania do dodania.
        """
        self.zadania.append(zadanie)

    
    def wyswietl_czas(self, **kwargs):
        """
        Funkcja wyswietl_czas.
        Funkcja wyswietla czas wykonania funkcji zapisywania zadan do pliku.        
        """
        if kwargs.get('start') and kwargs.get('koniec'):
            self.start = kwargs['start']
            self.koniec = kwargs['koniec']        

        print(f'Czas wykonania: {self.koniec - self.start} s.')

    def zapisz_do_pliku(self, nazwa_pliku='zadania.txt'):
        st = time()
        with open(nazwa_pliku, "a") as plik:
            for zadanie in self.zadania:
                plik.write(f"Tytuł: {zadanie.tytul}\n")
                plik.write(f"Opis: {zadanie.opis}\n")
                plik.write(f"Termin wykonania: {zadanie.termin}\n")
                if isinstance(zadanie, ZadaniePriorytetowe):
                    plik.write(f"Priorytet: {zadanie.priorytet}\n")
                elif isinstance(zadanie, ZadanieRegularne):
                    plik.write(f"Powtarzalność: {zadanie.powtarzalnosc}\n")
                plik.write('\n')
        self.zadania = []
        ko = time()
        self.wyswietl_czas(start=st, koniec=ko)        

    def odczytaj_z_pliku(self, nazwa_pliku='zadania.txt'):
        with open(nazwa_pliku, 'r') as plik:
            for each in plik:
                print(each)
                
            # linie = plik.readlines()
            # aktualne_zadanie = None
            # for linia in linie:
            #     linia = linia.strip()
            #     if linia.startswith("Tytuł: "):
            #         tytul = linia.replace("Tytuł: ", "")
            #         aktualne_zadanie = Zadanie(tytul, "", "")
            #     elif linia.startswith("Opis: "):
            #         opis = linia.replace("Opis: ", "")
            #         aktualne_zadanie.opis = opis
            #     elif linia.startswith("Termin wykonania: "):
            #         termin = linia.replace("Termin wykonania: ", "")
            #         aktualne_zadanie.termin = termin
            #         self.dodaj_zadanie(aktualne_zadanie)
            #     elif linia.startswith("Priorytet: "):
            #         priorytet = linia.replace("Priorytet: ", "")
            #         if aktualne_zadanie:
            #             zadanie_priorytetowe = ZadaniePriorytetowe(aktualne_zadanie.tytul, aktualne_zadanie.opis, aktualne_zadanie.termin, priorytet)
            #             self.zadania.pop()
            #             self.dodaj_zadanie(zadanie_priorytetowe)
            #     elif linia.startswith("Powtarzalność: "):
            #         powtarzalnosc = linia.replace("Powtarzalność: ", "")
            #         if aktualne_zadanie:
            #             zadanie_regularne = ZadanieRegularne(aktualne_zadanie.tytul, aktualne_zadanie.opis, aktualne_zadanie.termin, powtarzalnosc)
            #             self.zadania.pop()
            #             self.dodaj_zadanie(zadanie_regularne)

    """
    Funkcja usun_zadanie
    Funkcja usuwa zadania z pliku o nazwie zadania.txt
    """
    def usun_zadanie(self, tytul):
        for zadanie in self.zadania:
            if zadanie.tytul == tytul:
                self.zadania.remove(zadanie)
                return
            
        print("Zadanie o podanym tytule nie istnieje.")

    """
    Funkcja oznacz_jako_wykonane
    Funkcja sprawdza czy zadanie istnieje a potem zmienia jego status na wykonany.
    """
    def oznacz_jako_wykonane(self, tytul):
        for zadanie in self.zadania:
            if zadanie.tytul == tytul:
                zadanie.wykonane = True
                return
            
        print("Zadanie o podanym tytule nie istnieje.")

    """
    Funkcja edytuj_zadanie
    Funkcja edytuje zadanie na podstawie tytułu, jeżeli zadanie zostało znalezione, przypisuje nowe dane za pomoca słownika.
    """
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

    def __contains__(self, tytul):
        for zadanie in self.zadania:
            if zadanie.tytul == tytul:
                return True
            
        return False
