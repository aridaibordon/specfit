import matplotlib.pyplot as plt
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

from ui.components import TitledFrame


class TestMultizoneFrame(TitledFrame):
    def __init__(self, parent: tk.Frame):
        super().__init__(
            parent,
            title="Searching tools for plasma characterization (multizone scenario)",
        )
