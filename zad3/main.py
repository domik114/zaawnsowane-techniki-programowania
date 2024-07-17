import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

class Model:
    def __init__(self):
        self.image = None
        self.U = None
        self.S = None
        self.V = None
        self.fpath = None

    def load_image(self, file_path):
        try:
            self.image = Image.open(file_path)
            self.fpath = file_path
            self.U, self.S, self.V = self.svd_decomposition(self.image)
        except Exception as e:
            return str(e)
        return None

    def svd_decomposition(self, image, r=10):
        if image.mode == "L":
            image_array = np.array(image)
            U, S, Vt = np.linalg.svd(image_array, full_matrices=False)
            U = U[:, :r]
            S = np.diag(S[:r])
            Vt = Vt[:r, :]
            return U, S, Vt
        elif image.mode == "RGB":
            r_channel, g_channel, b_channel = image.split()
            r_array = np.array(r_channel)
            g_array = np.array(g_channel)
            b_array = np.array(b_channel)
            r_U, r_S, r_Vt = np.linalg.svd(r_array, full_matrices=False)
            g_U, g_S, g_Vt = np.linalg.svd(g_array, full_matrices=False)
            b_U, b_S, b_Vt = np.linalg.svd(b_array, full_matrices=False)
            r_U = r_U[:, :r]
            g_U = g_U[:, :r]
            b_U = b_U[:, :r]
            r_S = np.diag(r_S[:r])
            g_S = np.diag(g_S[:r])
            b_S = np.diag(b_S[:r])
            r_Vt = r_Vt[:r, :]
            g_Vt = g_Vt[:r, :]
            b_Vt = b_Vt[:r, :]
            return (r_U, g_U, b_U), (r_S, g_S, b_S), (r_Vt, g_Vt, b_Vt)
        else:
            raise ValueError("Unsupported image mode")

    def compress_image(self, r):
        if self.image.mode == "L":
            compressed_image_array = np.dot(self.U, np.dot(self.S, self.V))
            compressed_image = Image.fromarray(np.uint8(compressed_image_array))
            return compressed_image
        elif self.image.mode == "RGB":
            compressed_r_array = np.dot(self.U[0], np.dot(self.S[0], self.V[0]))
            compressed_g_array = np.dot(self.U[1], np.dot(self.S[1], self.V[1]))
            compressed_b_array = np.dot(self.U[2], np.dot(self.S[2], self.V[2]))
            compressed_r_image = Image.fromarray(np.uint8(compressed_r_array))
            compressed_g_image = Image.fromarray(np.uint8(compressed_g_array))
            compressed_b_image = Image.fromarray(np.uint8(compressed_b_array))
            compressed_image = Image.merge("RGB", (compressed_r_image, compressed_g_image, compressed_b_image))
            return compressed_image

class View:
    def __init__(self, root):
        self.root = root
        self.root.title("Obrazek Viewer")

        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack()

        self.load_button = tk.Button(root, text="Załaduj Obraz", command=self.load_image)
        self.load_button.pack()

        self.compress_button = tk.Button(root, text="Kompresuj Obraz", command=self.compress_image)
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

if __name__ == "__main__":
    root = tk.Tk()
    model = Model()
    view = View(root)
    presenter = Presenter(model, view)
    presenter.run()
