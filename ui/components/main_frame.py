import tkinter as tk

from tkinter import ttk


class TitledFrame(tk.Frame):
    def __init__(self, parent: tk.Frame, title: str):
        super().__init__(parent)

        frame_label = ttk.Label(self, text=title)
        frame_label.pack(fill="x")

        self.container = tk.Frame(self)
        self.container.pack(expand="True", fill="both", padx=20, pady=10)
