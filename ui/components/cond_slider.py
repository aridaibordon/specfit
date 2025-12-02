import customtkinter as ctk


class LabeledSlider:
    def __init__(self, parent, text, **slider_kwargs):
        self.label = ctk.CTkLabel(parent, text=text)
        self.slider = ctk.CTkSlider(parent, **slider_kwargs)
        self.slider.set(0)
