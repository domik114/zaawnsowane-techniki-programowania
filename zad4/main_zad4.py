import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import time

def obiekt_dynamiczny(t, stan, m, c, k, A, f):
    """
    Funkcja opisująca dynamiczny system za pomocą równań różniczkowych.

    Parametry:
    - t: czas
    - stan: lista dwóch elementów, zawierająca przemieszczenie (x) i prędkość (v)
    - m: masa
    - c: współczynnik tłumienia/tarcia
    - k: współczynnik sztywności sprężyny
    - A: amplituda siły zewnętrznej
    - f: częstotliwość siły zewnętrznej

    Zwraca:
    Lista dwóch wartości: prędkości i przemieszczenia.
    """
    x, v = stan
    F = A * np.sin(2 * np.pi * f * t)
    dxdt = v
    dvdt = (F - c * v - k * x) / m
    return [dxdt, dvdt] # pochodne przemieszczenia i prędkości

def sim(m, c, k, A, f):
    """
    Funkcja symulująca zachowanie dynamicznego systemu.

    Parametry:
    - m: masa
    - c: współczynnik tłumienia/tarcia
    - k: współczynnik sztywności sprężyny
    - A: amplituda siły zewnętrznej
    - f: częstotliwość siły zewnętrznej

    Zwraca:
    Tuple zawierający maksymalne przemieszczenie i czas wykonania symulacji.
    """
    warunki_poczatkowe = [0, 0]
    punkty_czasu = np.arange(0, 10, 0.01)
    
    start_time = time.time()
    # rozwiazuje uklad rozn, przekazuje funkcje obiekt dynmiczny, przedzial czasowy war poczatkowe, punkty czasu oraz parametry
    wynik = solve_ivp(obiekt_dynamiczny, [0, 10], warunki_poczatkowe, t_eval=punkty_czasu, args=(m, c, k, A, f))
    end_time = time.time()
    
    # oblicza max przemieszczenie biorąc maksymalną wartość bezwzględną z przemieszczenia
    max_przemieszczenie = np.max(np.abs(wynik.y[0]))
    
    return max_przemieszczenie, end_time - start_time

def main():
    m_wartosci = np.linspace(1, 10, 100)
    f_wartosci = np.linspace(1, 10, 100)
    c = 0.001
    k = 1000
    A = 1
    
    start_time = time.time()
    wyniki_sekwencyjne = []
    for m in m_wartosci:
        for f in f_wartosci:
            wynik = sim(m, c, k, A, f)
            wyniki_sekwencyjne.append((m, f, wynik[0], wynik[1]))
    end_time = time.time()

    print(f"Czas {end_time - start_time}")

    rys_plot(wyniki_sekwencyjne, "Symulacja sekwencyjna")

    plt.show()

def rys_plot(wyniki, tytul):
    m_wartosci = np.unique([wynik[0] for wynik in wyniki]) # unikalna lista mas
    f_wartosci = np.unique([wynik[1] for wynik in wyniki]) # unikalna lista czestotliwosci
    max_przemieszczenia = np.array([wynik[2] for wynik in wyniki]).reshape(len(m_wartosci), len(f_wartosci)) # macierz maksymalnych przemieszczen 

    plt.pcolormesh(f_wartosci, m_wartosci, max_przemieszczenia.T)
    plt.colorbar(label='Maksymalne Przemieszczenie')
    plt.xlabel('Częstotliwość (Hz)')
    plt.ylabel('Masa (kg)')
    plt.title(tytul)
    plt.show()

if __name__ == "__main__":
    main()
