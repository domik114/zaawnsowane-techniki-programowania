import random
import numpy as np
import time

def monte_carlo(a, b, n):
    """
    Funkcja Monte Carlo w czystym pythonie.
    """
    suma = 0

    for _ in range(n):
        x = random.uniform(a, b)
        suma += x**2

    wynik = (b - a) * suma / n

    return wynik

def monte_carlo_numpy(a, b, n):
    """
    Funkcja Monte Carlo w numpy.
    """
    x = np.random.uniform(a, b, n)
    suma = np.sum(x**2)
    wynik = (b - a) * suma / n

    return wynik

start = time.time()
wynik = monte_carlo(0, 2, 10000000)
koniec = time.time()
print(f"wynik: {wynik}, czas: {koniec - start:.4f}")

start = time.time()
wynik_numpy = monte_carlo_numpy(0, 2, 10000000)
koniec = time.time()
print(f"wynik: {wynik}, czas: {koniec-start:.4f} numpy")