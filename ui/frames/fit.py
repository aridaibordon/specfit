import logging

import tkinter as tk
import matplotlib.pyplot as plt

from tkinter import filedialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ui.components import CondSlider


COND_SLIDER_CONFIG = {
    "t_elec": {"text": "Electron temperature (eV):"},
    "d_elec": {"text": "Electron density (/cc):"},
    "clength": {"text": "Characteristic plasma length (cm):"},
}


class FitFrame(tk.Frame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)

        self.fig, self.ax = plt.subplots(figsize=(6, 6), tight_layout=True)
        self.text = self.ax.text(0.02, 0.98, s="", transform=self.ax.transAxes, ha="left", va="top")

        # Canvas container
        canvas_container = tk.Frame(self)
        canvas_container.pack(expand=True, side=tk.LEFT)

        self.canvas = FigureCanvasTkAgg(self.fig, canvas_container)
        canvas_lower_container = tk.Frame(canvas_container)
        canvas_checkbox_container = tk.Frame(canvas_lower_container)

        self.xscale_log = tk.BooleanVar(value=False)
        self.yscale_log = tk.BooleanVar(value=False)

        checkbox_xscale = ttk.Checkbutton(
            canvas_checkbox_container,
            variable=self.xscale_log,
            text="x log scale",
            command=self.update_scale,
        )
        checkbox_yscale = ttk.Checkbutton(
            canvas_checkbox_container,
            variable=self.yscale_log,
            text="y log scale",
            command=self.update_scale,
        )
        save_fig_button = ttk.Button(
            canvas_lower_container, width=20, text="Save figure", command=self.save_fig
        )

        checkbox_xscale.pack(padx=3, pady=1, side=tk.LEFT)
        checkbox_yscale.pack(padx=3, pady=1, side=tk.LEFT)
        save_fig_button.pack(side=tk.RIGHT)

        self.canvas.get_tk_widget().pack()
        canvas_lower_container.pack(padx=10, pady=10, fill="x")
        canvas_checkbox_container.pack(anchor="w")

        # Slider container
        slider_container = tk.Frame(self)
        slider_container.pack(expand=True, side=tk.RIGHT)

        slider_label1 = ttk.Label(slider_container, text="electron temperature (eV)")
        slider_label2 = ttk.Label(slider_container, text="electron density (/cc)")
        slider_label3 = ttk.Label(slider_container, text="characteristic length (cm)")

        slider1 = ttk.Scale(
            slider_container, command=lambda val: self.redraw_canvas("attr1", val)
        )
        slider2 = ttk.Scale(slider_container)
        slider3 = ttk.Scale(slider_container)

        for ind, (slider_label, slider) in enumerate(
            zip(
                [slider_label1, slider_label2, slider_label3],
                [slider1, slider2, slider3],
            )
        ):
            slider_label.grid(row=ind, column=0, padx=10, pady=5, sticky="w")
            slider.grid(row=ind, column=1)

    def redraw_canvas(self, attr: str, val: str) -> None:
        self.text.set_text(f"$T_e = {float(val):.2f}$ eV")
        self.canvas.draw()

    def update_scale(self) -> None:
        self.ax.set_xscale("log" if self.xscale_log.get() else "linear")
        self.ax.set_yscale("log" if self.yscale_log.get() else "linear")

        self.canvas.draw()

    def save_fig(self):
        figname = filedialog.asksaveasfilename()
        if figname:
            self.fig.savefig(figname)
