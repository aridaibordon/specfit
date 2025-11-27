import tkinter as tk
from tkinter import ttk


class CondSlider(tk.Frame):
    def __init__(self, parent, text):
        super().__init__(parent)

        self.label = tk.Label(self, text=text)
        self.label.pack(side="top")

        self.slider = ttk.Scale(self, length=300)
        self.slider.pack(side="top")
