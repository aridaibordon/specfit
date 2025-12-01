import logging

from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

from tkinter import filedialog, ttk
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
        "unit": "cm$^{{-3}}$",
    },
    "clength": {
        "text": "Characteristic plasma length (cm): ",
        "tex_symbol": "L",
        "unit": "cm",
    },
}

TAB_TEV = np.linspace(1, 20, 10)


class TestFitFrame(TitledFrame):
    def __init__(self, parent: tk.Frame):
        super().__init__(parent, title="Manual fitting")

        self.db = self.load_database()
        self.tab = self.db.get_data_tables()

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=3, uniform="fit_frame")
        self.container.grid_rowconfigure(1, weight=2, uniform="fit_frame")

        self.create_figure()
        self.create_canvas()
        self.create_manager()

        self.update_cond_label()

    def __post_init__(self):
        self.update_canvas()

    def load_database(self):
        db_path = config.read_entry("db")
        if not db_path:
            logging.warning("Database is not specified in configuration file.")
            return

        return SpecFitDatabase(db_path)

    def create_figure(self) -> None:
        self.fig, self.ax = plt.subplots(figsize=(6, 4), tight_layout=True)

        self.cond_label = self.ax.text(
            0.5,
            1.02,
            s="",
            transform=self.ax.transAxes,
            ha="center",
            va="bottom",
        )

        x_exp, y_exp = self.db.get_experimental_sample(1)
        (self.l_sample,) = self.ax.plot(
            x_exp, y_exp, ".", ms=2, label="experimental data"
        )

        egrid, signal = self.db.get_synthetic_signal(
            sample=1,
            t_ind=0,
            d_ind=0,
            clenght_ind=0,
        )
        (self.l_fit,) = self.ax.plot(
            egrid, signal, lw=2, alpha=0.8, label="synthetic spectra"
        )

        self.ax.set_xlabel("Photon energy (eV)")
        self.ax.set_ylabel("Intensity (arb. units)")

        self.ax.set_xlim(np.min(x_exp), np.max(x_exp))

        self.ax.legend()

    def create_canvas(self) -> None:
        canvas_container = tk.Frame(self.container)
        canvas_container.grid(column=0, row=0, sticky="nwes", padx=100)

        self.canvas = FigureCanvasTkAgg(self.fig, canvas_container)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        canvas_options = tk.Frame(canvas_container, pady=5)
        canvas_checkbox = tk.Frame(canvas_options)

        self.xscale_log = tk.BooleanVar(value=False)
        self.yscale_log = tk.BooleanVar(value=False)

        checkbox_xscale = ttk.Checkbutton(
            canvas_checkbox,
            variable=self.xscale_log,
            text="x log scale",
            command=self.update_canvas_scale,
        )
        checkbox_yscale = ttk.Checkbutton(
            canvas_checkbox,
            variable=self.yscale_log,
            text="y log scale",
            command=self.update_canvas_scale,
        )

        save_fig_button = ttk.Button(
            canvas_options, text="Save figure", command=self.save_fig
        )

        canvas_options.pack(fill="x", padx=10)
        canvas_options.grid_columnconfigure((0, 1), weight=1)

        canvas_checkbox.grid(column=0, row=0, sticky="w")
        checkbox_xscale.pack(side=tk.LEFT)
        checkbox_yscale.pack(side=tk.LEFT, padx=5)
        save_fig_button.grid(column=1, row=0, sticky="e")

    def create_manager(self) -> None:
        manager_container = ttk.Frame(self.container)
        manager_container.grid(column=0, row=1, sticky="we", padx=100)

        manager_container_label = ttk.Label(manager_container, text="Options manager")
        manager_container_label.pack(fill="x")

        manager_grid_container = ttk.Frame(manager_container)
        manager_grid_container.pack(expand=True, fill="both")

        manager_grid_container.grid_rowconfigure(0, weight=1, uniform="mg_container")
        manager_grid_container.grid_rowconfigure(1, weight=2, uniform="mg_container")
        manager_grid_container.grid_columnconfigure(
            (0, 1, 2), weight=1, uniform="mg_container"
        )

        sample_selector_container = tk.Frame(manager_grid_container)
        sample_selector_container.grid(column=0, row=0, sticky="nwes")

        sample_selector_center = tk.Frame(sample_selector_container)
        sample_selector_center.pack(expand=True)

        sample_selector_label = ttk.Label(
            sample_selector_center, text="Experimental sample: "
        )
        self.sample_selector = ttk.Spinbox(
            sample_selector_center,
            width=2,
            from_=1,
            to=7,
            command=self.update_canvas,
        )
        self.sample_selector.set(1)

        sample_selector_label.pack(side=tk.LEFT, padx=10)
        self.sample_selector.pack(side=tk.LEFT, padx=10)

        geometry_selector_container = tk.Frame(manager_grid_container)
        geometry_selector_container.grid(column=1, row=0, sticky="nwes")

        geometry_selector_center = tk.Frame(geometry_selector_container)
        geometry_selector_center.pack(expand=True)

        geometry_selector_label = ttk.Label(geometry_selector_center, text="Geometry: ")
        self.geometry_selector = ttk.Combobox(
            geometry_selector_center,
            width=10,
            values=["Cylindrical", "Spherical", "Planar"],
            justify="center",
            # command=self.update_geometry --command not supported
        )
        self.geometry_selector.current(2)

        geometry_selector_label.pack(side=tk.LEFT, padx=10)
        self.geometry_selector.pack(side=tk.LEFT, padx=10)

        mc_selector_container = tk.Frame(manager_grid_container)
        mc_selector_container.grid(column=2, row=0, sticky="nwes")

        mc_selector_center = tk.Frame(mc_selector_container)
        mc_selector_center.pack(expand=True)

        self.mc_val = tk.BooleanVar(value=False)
        mc_selector_label = ttk.Label(
            mc_selector_center, text="Assume mass conservation: "
        )
        mc_selector = ttk.Checkbutton(
            mc_selector_center,
            variable=self.mc_val,
            command=self.update_mc_selector,
        )

        mc_selector_label.pack(side=tk.LEFT, padx=10)
        mc_selector.pack(side=tk.LEFT, padx=10)

        slider_container = tk.Frame(manager_grid_container)
        slider_container.grid(column=0, row=1, columnspan=3, sticky="nwes", pady=5)

        slider_container_center = tk.Frame(slider_container)
        slider_container_center.pack(expand=True)

        self.slider: Dict[str, LabeledSlider] = {}
        for ind, key in enumerate(SLIDERS_CONFIG):
            labeled_slider = LabeledSlider(
                slider_container_center,
                text=SLIDERS_CONFIG[key]["text"],
                length=250,
                to=len(self.tab[key]) - 1,
                command=lambda val: self.update_canvas(),
            )
            self.slider[key] = labeled_slider

            labeled_slider.label.grid(row=ind, column=0, padx=10, pady=5, sticky="w")
            labeled_slider.slider.grid(row=ind, column=1, padx=10, pady=5, sticky="e")

    def update_geometry(self):
        print(self.geometry_selector.get())
        config.add_entry("geometry", self.geometry_selector.get())

    def update_mc_selector(self):
        if self.mc_val.get():
            self.slider["clength"].label.grid_remove()
            self.slider["clength"].slider.grid_remove()
        else:
            self.slider["clength"].label.grid()
            self.slider["clength"].slider.grid()

    def update_canvas(self):
        sample = int(self.sample_selector.get())
        t_ind, d_ind, clength_ind = self.get_current_indexes()

        x_exp, y_exp = self.db.get_experimental_sample(sample)
        egrid, signal = self.db.get_synthetic_signal(sample, t_ind, d_ind, clength_ind)

        self.l_sample.set_xdata(x_exp)
        self.l_sample.set_ydata(y_exp)
        self.l_fit.set_xdata(egrid)
        self.l_fit.set_ydata(signal)

        self.update_cond_label()

        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def update_cond_label(self) -> None:
        text_attr = []
        for attr, labeled_slider in self.slider.items():
            attr_tab = self.tab[attr]
            attr_val = attr_tab[round(labeled_slider.slider.get())]

            sym, unit = SLIDERS_CONFIG[attr]["tex_symbol"], SLIDERS_CONFIG[attr]["unit"]
            fmt = f"{attr_val:.2e}" if attr == "d_elec" else f"{attr_val:.2f}"

            text_attr.append(f"${sym} =$ {fmt} {unit}")

        s = f"Sample {self.sample_selector.get()}: " + ", ".join(text_attr)
        self.cond_label.set_text(s)

    def update_canvas_scale(self) -> None:
        self.ax.set_xscale("log" if self.xscale_log.get() else "linear")
        self.ax.set_yscale("log" if self.yscale_log.get() else "linear")

        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def get_current_indexes(self) -> List[int]:
        return [
            round(labeled_slider.slider.get())
            for labeled_slider in self.slider.values()
        ]

    def save_fig(self) -> None:
        figname = filedialog.asksaveasfilename()
        if figname:
            self.fig.savefig(figname)
