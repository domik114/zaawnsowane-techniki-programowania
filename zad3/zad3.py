import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import unittest

class Model:
    """
    Klasa Modelu do kompresji obrazu przy użyciu SVD.
    """

    def __init__(self):
        self.image = None
        self.U = None
        self.S = None
        self.V = None
        self.fpath = None

    def load_image(self, file_path):
        """
        Wczytaj obraz i wykonaj dekompozycję SVD.

        Args:
            file_path (str): Ścieżka do pliku obrazu.

        Returns:
            str: Komunikat o błędzie, jeśli wczytywanie lub dekompozycja nie powiedzie się, w przeciwnym razie None.
        """
        try:
            self.image = Image.open(file_path)
            self.fpath = file_path
        except Exception as e:
            return str(e)
        return None

    def svd_decomposition(self, image, r=10):
        """
        Przeprowadź dekompozycję SVD na podanym obrazie.

        Args:
            image (PIL.Image): Wejściowy obraz.
            r (int): Liczba wartości osobliwych do zachowania.

        Returns:
            tuple: Krotka macierzy U, S i V dla obrazu w odcieniach szarości lub RGB.
        """
        if image.mode == "L":
            image_array = np.array(image)
            U, S, Vt = np.linalg.svd(image_array, full_matrices=False)
            U = U[:, :r]
            S = np.diag(S[:r])
            Vt = Vt[:r, :]
            return U, S, Vt
        elif image.mode == "RGB":
            r_channel, g_channel, b_channel = image.split() # rozdzelenie obrazu na kanaly r g b
            r_array = np.array(r_channel)
            g_array = np.array(g_channel)
            b_array = np.array(b_channel)
            r_U, r_S, r_Vt = np.linalg.svd(r_array, full_matrices=False) # przeprowadzenie dekompozycji
            g_U, g_S, g_Vt = np.linalg.svd(g_array, full_matrices=False)
            b_U, b_S, b_Vt = np.linalg.svd(b_array, full_matrices=False)
            r_U = r_U[:, :r] # ograniczenie liczby kolumn do pierwszego r
            g_U = g_U[:, :r]
            b_U = b_U[:, :r]
            r_S = np.diag(r_S[:r]) # ograniczenie liczby wartości osbliwych do pierwszego r
            g_S = np.diag(g_S[:r]) # i utworzenie macierzy diagonalnej
            b_S = np.diag(b_S[:r])
            r_Vt = r_Vt[:r, :] # ograniczenie wierszy dla pierwszych r
            g_Vt = g_Vt[:r, :]
            b_Vt = b_Vt[:r, :]
            return (r_U, g_U, b_U), (r_S, g_S, b_S), (r_Vt, g_Vt, b_Vt)
        else:
            raise ValueError("Unsupported image mode")

    def compress_image(self, r):
        """
        Kompresuj obraz przy użyciu określonej liczby wartości osobliwych.

        Args:
            r (int): Liczba wartości osobliwych do zachowania.

        Returns:
            PIL.Image: Kompresowany obraz.
        """

        self.U, self.S, self.V = self.svd_decomposition(self.image, r)
        if self.image.mode == "L":
            compressed_image_array = np.dot(self.U, np.dot(self.S, self.V)) # kompresja obrazu poprzez mnożenie macierzy i uzyskanie zrekonstruowanej macierzy obrazu
            compressed_image = Image.fromarray(np.uint8(compressed_image_array)) # konwersja zrek. macierzy obrazu
            return compressed_image
        elif self.image.mode == "RGB":
            compressed_r_array = np.dot(self.U[0], np.dot(self.S[0], self.V[0])) # kompresja kanału
            compressed_g_array = np.dot(self.U[1], np.dot(self.S[1], self.V[1]))
            compressed_b_array = np.dot(self.U[2], np.dot(self.S[2], self.V[2]))
            compressed_r_image = Image.fromarray(np.uint8(compressed_r_array)) # konwersja zrek. macierzy kanału
            compressed_g_image = Image.fromarray(np.uint8(compressed_g_array))
            compressed_b_image = Image.fromarray(np.uint8(compressed_b_array))
            compressed_image = Image.merge("RGB", (compressed_r_image, compressed_g_image, compressed_b_image)) # scalanie skompresowanych kanałów do jednego obrazu w formacie rgb
            return compressed_image

class View:
    """
    Klasa Prezentera do zarządzania interakcjami między modelem a widokiem.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack()

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.compress_button = tk.Button(root, text="Compress Image", command=self.compress_image)
        self.compress_button.pack()

        self.r_entry = tk.Entry(root)
        self.r_entry.insert(0, "10")
        self.r_entry.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.bmp *.png")])
        if file_path:
            self.presenter.load_image(file_path)

    def compress_image(self):
        r = int(self.r_entry.get())
        compressed_image = self.presenter.compress_image(r)
        self.display_image(compressed_image)

    def display_image(self, image):
        self.canvas.delete("all")
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.canvas.image = self.photo

class Presenter:
    """
    Klasa Prezentera do zarządzania interakcjami między modelem a widokiem.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.presenter = self

    def load_image(self, file_path):
        error_message = self.model.load_image(file_path)
        if error_message:
            self.view.display_error(error_message)
        else:
            self.view.display_image(self.model.image)

    def compress_image(self, r):
        return self.model.compress_image(r)

    def run(self):
        self.view.root.mainloop()

class TestImageCompression(unittest.TestCase):
    """
    Unit tests for the Image Compression application.
    """

    def test_image_loading(self):
        model = Model()
        error_message = model.load_image("nonexistent_image.jpg")
        self.assertIsNotNone(error_message)
        print("test 1")

    def test_svd_decomposition(self):
        model = Model()
        image = Image.new("L", (100, 100))
        U, S, Vt = model.svd_decomposition(image, r=10)
        self.assertIsNotNone(U)
        self.assertIsNotNone(S)
        self.assertIsNotNone(Vt)
        print("test 2")

if __name__ == "__main__":
    root = tk.Tk()
    model = Model()
    view = View(root)
    presenter = Presenter(model, view)
    presenter.run()

    test = TestImageCompression()
    test.test_image_loading()    
    test.test_svd_decomposition()