import tkinter as tk
from tkinter import ttk


class LabeledSlider:
    def __init__(self, parent, text, **slider_kwargs):
        self.label = ttk.Label(parent, text=text)
        self.slider = ttk.Scale(parent, **slider_kwargs)
