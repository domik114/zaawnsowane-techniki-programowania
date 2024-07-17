from zadania import Zadanie, ZadaniePriorytetowe, ZadanieRegularne, ManagerZadan
from os import system
from time import sleep

def menu():
    system('cls')
    print("1. Dodaj nowe zadanie")
    print("2. Usuń zadanie")
    print("3. Oznacz zadanie jako wykonane")
    print("4. Edytuj zadanie")
    print("5. Wyświetl listę zadań")
    print("6. Sortuj zadania")
    print("7. Wyjdź")

if __name__ == "__main__":
    mg_zadan = ManagerZadan()

    while True:
        menu()
        opcja = input("\nWybierz opcję: ")

        if opcja == "1":
            tytul = input("\nPodaj tytuł zadania: ")
            opis = input("Podaj opis zadania: ")
            termin = input("Podaj termin wykonania zadania (RRRR-MM-DD): ")
            priorytet = input("Podaj priorytet zadania (opcjonalne): ")
            powtarzalnosc = input("Podaj powtarzalność zadania (opcjonalne): ")

            if not mg_zadan.__contatins__(tytul):
                if priorytet:
                    zadanie = ZadaniePriorytetowe(tytul, opis, termin, priorytet)
                elif powtarzalnosc:
                    zadanie = ZadanieRegularne(tytul, opis, termin, powtarzalnosc)
                else:
                    zadanie = Zadanie(tytul, opis, termin)

                mg_zadan.dodaj_zadanie(zadanie)
                print("\nZadanie zostało dodane.\n")
            else:
                print("\nZadanie o podanym tytule już istnieje.\n")
            sleep(2)

        elif opcja == "2":
            tytul = input("\nPodaj tytuł zadania do usunięca: ")
            mg_zadan.usun_zadanie(tytul)
            sleep(2)
            
        elif opcja == "3":
            tytul = input("Podaj tytuł zadania do oznaczenia jako wykonane: ")
            mg_zadan.oznacz_jako_wykonane(tytul)
            sleep(2)

        elif opcja == "4":
            tytul = input("Podaj tytuł zadania do edycji: ")
            nowe_dane = {}
            nowe_dane['tytul'] = input("Nowy tytuł zadania : ")
            nowe_dane['opis'] = input("Nowy opis zadania  ")
            nowe_dane['termin'] = input("Nowy termin wykonania zadania (RRRR-MM-DD): ")

            priorytet = input("Nowy priorytet zadania: ")            
            if priorytet:
                nowe_dane['priorytet'] = priorytet
                
            powtarzalnosc = input("Nowa powtarzalność zadania: ")
            if powtarzalnosc:
                nowe_dane['powtarzalnosc'] = powtarzalnosc

            mg_zadan.edytuj_zadanie(tytul, nowe_dane)
            print("Zadanie zaktualizowane.")
            sleep(2)

        elif opcja == "5":
            for i, zadanie in enumerate(mg_zadan.zadania, 1):
                print(f"\nZadanie {i}: \n{zadanie}")
            sleep(3)

        elif opcja == "6":
            mg_zadan.sortuj()
            print("\nZadania zostały posortowanie według daty.\n")
            sleep(2)

        elif opcja == "7":
            break

        else:
            print("\nNieprawidłowa opcja. Wybierz ponownie\n")
            sleep(2)