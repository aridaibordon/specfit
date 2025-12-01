import logging
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import customtkinter as ctk

from customtkinter import filedialog
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
from logic.database import SpecFitDatabase
from ui.components import TitledFrame, LabeledSlider


SLIDERS_CONFIG = {
    "t_elec": {
        "text": "Electron temperature (eV): ",
        "tex_symbol": "T_e",
        "unit": "eV",
        "fmt": "3f",
    },
    "d_elec": {
        "text": "Electron density (/cc): ",
        "tex_symbol": "n_e",
        "unit": "cm$^{-3}$",
    },
    "clength": {
        "text": "Characteristic plasma length (cm): ",
        "tex_symbol": "L",
        "unit": "cm",
    },
}

TAB_TEV = np.linspace(1, 20, 10)


class TestFitFrame(TitledFrame):
    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent, title="Manual fitting")

        self.db = self.load_database()

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=3)
        self.container.grid_rowconfigure(1, weight=2)

        self.create_figure()
        self.create_canvas()
        self.create_manager()
        self.update_cond_label()

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------
    def load_database(self):
        db_path = config.read_entry("db")
        if not db_path:
            logging.warning("Database is not specified in configuration.")
            return None
        return SpecFitDatabase(db_path)

    # ----------------------------------------------------------
    # Figure
    # ----------------------------------------------------------
    def create_figure(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4), tight_layout=True)
        self.cond_label = self.ax.text(
            0.5, 1.02, "", transform=self.ax.transAxes, ha="center", va="bottom"
        )
        self.ax.set_xlabel("Photon energy (eV)")
        self.ax.set_ylabel("Intensity (arb. units)")

    def create_canvas(self):
        canvas_container = ctk.CTkFrame(self.container)
        canvas_container.grid(row=0, column=0, sticky="nwes", padx=100)

        self.canvas = FigureCanvasTkAgg(self.fig, canvas_container)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        options = ctk.CTkFrame(canvas_container)
        options.pack(fill="x", padx=10, pady=5)

        options.grid_columnconfigure((0, 1), weight=1)

        # Checkboxes
        checkbox_frame = ctk.CTkFrame(options)
        checkbox_frame.grid(row=0, column=0, sticky="w")

        self.xscale_log = ctk.BooleanVar(value=False)
        self.yscale_log = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(
            checkbox_frame,
            text="x log scale",
            variable=self.xscale_log,
            command=self.update_canvas_scale,
        ).pack(side=ctk.LEFT)

        ctk.CTkCheckBox(
            checkbox_frame,
            text="y log scale",
            variable=self.yscale_log,
            command=self.update_canvas_scale,
        ).pack(side=ctk.LEFT, padx=5)

        # Save button
        ctk.CTkButton(options, text="Save figure", command=self.save_fig).grid(
            row=0, column=1, sticky="e"
        )

    # ----------------------------------------------------------
    # Manager section
    # ----------------------------------------------------------
    def create_manager(self):
        manager_container = ctk.CTkFrame(self.container)
        manager_container.grid(row=1, column=0, sticky="we", padx=100)

        ctk.CTkLabel(manager_container, text="Options manager").pack(fill="x")

        manager_grid = ctk.CTkFrame(manager_container)
        manager_grid.pack(expand=True, fill="both")

        manager_grid.grid_columnconfigure((0, 1, 2), weight=1)
        manager_grid.grid_rowconfigure(0, weight=1)
        manager_grid.grid_rowconfigure(1, weight=2)

        # --------- Sample selector ----------
        sample_frame = ctk.CTkFrame(manager_grid)
        sample_frame.grid(row=0, column=0, sticky="nwes")

        center = ctk.CTkFrame(sample_frame)
        center.pack(expand=True)

        ctk.CTkLabel(center, text="Experimental sample:").pack(side=ctk.LEFT, padx=10)

        self.sample_selector = ttk.Spinbox(
            center, from_=1, to=7, width=60, command=self.update_canvas
        )
        self.sample_selector.set(1)
        self.sample_selector.pack(side=ctk.LEFT, padx=10)

        # --------- Geometry selector ----------
        geom_frame = ctk.CTkFrame(manager_grid)
        geom_frame.grid(row=0, column=1, sticky="nwes")

        center = ctk.CTkFrame(geom_frame)
        center.pack(expand=True)

        ctk.CTkLabel(center, text="Geometry:").pack(side=ctk.LEFT, padx=10)

        self.geometry_selector = ctk.CTkOptionMenu(
            center, values=["Cylindrical", "Spherical", "Planar"], width=120
        )
        self.geometry_selector.set("Planar")
        self.geometry_selector.pack(side=ctk.LEFT, padx=10)

        # --------- Mass conservation ----------
        mc_frame = ctk.CTkFrame(manager_grid)
        mc_frame.grid(row=0, column=2, sticky="nwes")

        center = ctk.CTkFrame(mc_frame)
        center.pack(expand=True)

        self.mc_val = ctk.BooleanVar(value=False)

        ctk.CTkLabel(center, text="Assume mass conservation:").pack(side=ctk.LEFT)
        ctk.CTkCheckBox(
            center, variable=self.mc_val, command=self.update_mass_conservation
        ).pack(side=ctk.LEFT, padx=10)

        # --------- Sliders ----------
        slider_frame = ctk.CTkFrame(manager_grid)
        slider_frame.grid(row=1, column=0, columnspan=3, sticky="nwes", pady=5)

        slider_center = ctk.CTkFrame(slider_frame)
        slider_center.pack(expand=True)

        self.slider: Dict[str, LabeledSlider] = {}
        for r, key in enumerate(SLIDERS_CONFIG):
            labeled = LabeledSlider(
                slider_center,
                text=SLIDERS_CONFIG[key]["text"],
                length=250,
                to=len(TAB_TEV) - 1,
                command=lambda v, a=key: self.update_canvas(),
            )
            self.slider[key] = labeled

            labeled.label.grid(row=r, column=0, padx=10, pady=5, sticky="w")
            labeled.slider.grid(row=r, column=1, padx=10, pady=5, sticky="e")

    # ----------------------------------------------------------
    # Updates
    # ----------------------------------------------------------
    def update_mass_conservation(self):
        """Hide or show one slider depending on checkbox."""
        if self.mc_val.get():
            self.slider["clength"].label.grid_remove()
            self.slider["clength"].slider.grid_remove()
        else:
            self.slider["clength"].label.grid()
            self.slider["clength"].slider.grid()

    def update_canvas(self):
        self.update_cond_label()
        self.canvas.draw()

    def update_cond_label(self):
        text_attr = []
        for attr, slider in self.slider.items():
            idx = round(slider.slider.get())
            val = TAB_TEV[idx]

            if attr == "d_elec":
                fmt = f"{val:.2e}"
            else:
                fmt = f"{val:.2f}"

            info = SLIDERS_CONFIG[attr]
            text_attr.append(f"${info['tex_symbol']} = $ {fmt} {info['unit']}")

        s = f"sample {self.sample_selector.get()}: " + ", ".join(text_attr)
        self.cond_label.set_text(s)

    def update_canvas_scale(self):
        self.ax.set_xscale("log" if self.xscale_log.get() else "linear")
        self.ax.set_yscale("log" if self.yscale_log.get() else "linear")
        self.canvas.draw()

    # ----------------------------------------------------------
    def save_fig(self):
        figname = filedialog.asksaveasfilename()
        if figname:
            self.fig.savefig(figname)
