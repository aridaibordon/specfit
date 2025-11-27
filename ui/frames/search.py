import tkinter as tk

from pathlib import Path
from tkinter import filedialog, ttk

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
from ui.components import CondSlider


COND_SLIDER_CONFIG = {
    "t_elec": {"text": "Electron temperature (eV):"},
    "d_elec": {"text": "Electron density (/cc):"},
    "clength": {"text": "Characteristic plasma length (cm):"},
}

def select_database():
    db_dialog = filedialog.askdirectory(title="Select spectral database folder")
    if not db_dialog:
        return

    db_path = Path(db_dialog)

    config.add_entry("db", db_dialog)


class CanvasSubframe(tk.Frame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)

        fig, ax = plt.subplots(tight_layout=True)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)


class SliderSubframe(tk.Frame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)

        sliders = {
            key: CondSlider(self, **COND_SLIDER_CONFIG[key])
            for key in ["t_elec", "d_elec", "clength"]
        }

        for slider in sliders.values():
            slider.pack()

"""
class SearchFrame(tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)

        figure_container = CanvasSubframe(self)
        slider_container = SliderSubframe(self)

        database_btn = tk.Button(slider_container, text="Select database", command=select_database)
        database_btn.pack()

        fig, ax = plt.subplots(tight_layout=True)

        canvas = FigureCanvasTkAgg(fig, figure_container)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)

        figure_container.pack()
        slider_container.pack()
"""

class SearchFrame(tk.Frame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)

        fig, ax = plt.subplots(figsize=(3, 2), tight_layout=True)

        canvas_container = tk.Frame(self)
        canvas_container.pack()

        canvas = FigureCanvasTkAgg(fig, canvas_container)
        canvas.get_tk_widget().pack()
