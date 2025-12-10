import logging

from typing import Dict, List

import customtkinter as ctk
import matplotlib.pyplot as plt

from customtkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config

from logic.database import load_database
from ui.components import TitledFrame, LabeledSlider


SLIDERS_CONFIG = {
    "t_elec": {
        "text": "Electron temperature (eV): ",
        "tex_symbol": "T_e",
        "unit": "eV",
        "fmt": ".2f",
    },
    "d_elec": {
        "text": "Electron density (/cc): ",
        "tex_symbol": "n_e",
        "unit": "cm$^{{-3}}$",
        "fmt": ".2f",
    },
    "clength": {
        "text": "Characteristic plasma length (cm): ",
        "tex_symbol": "L",
        "unit": "cm",
        "fmt": ".2f",
    },
}


class FitFrame(TitledFrame):
    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent, title="Manual fitting")

        self.db = load_database(db_path=config.read_entry("db"))
        self.tab = self.db.get_data_tables()

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=3, uniform="fit_frame")
        self.container.grid_rowconfigure(1, weight=2, uniform="fit_frame")

        self.create_figure()
        self.create_canvas()
        self.create_manager()

        self.update_cond_label()
        self.update_mc_selector()

    def __post_init__(self):
        self.update_canvas()

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
            clength_ind=0,
            geometry=config.read_entry("geometry"),
        )
        (self.l_fit,) = self.ax.plot(
            egrid, signal, lw=2, alpha=0.8, label="synthetic spectra"
        )

        self.ax.set_xlabel("Photon energy (eV)")
        self.ax.set_ylabel("Intensity (arb. units)")

        self.ax.set_xlim(*self.db.config["plot"]["xlim"])

        self.ax.legend()

    def create_canvas(self) -> None:
        canvas_container = ctk.CTkFrame(self.container, fg_color="transparent")
        canvas_container.grid(column=0, row=0, sticky="nwes", padx=100)

        self.canvas = FigureCanvasTkAgg(self.fig, canvas_container)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        canvas_options = ctk.CTkFrame(canvas_container, fg_color="transparent")
        canvas_checkbox = ctk.CTkFrame(canvas_options, fg_color="transparent")
        save_fig_button = ctk.CTkButton(
            canvas_options,
            text="Save figure",
            width=110,
            height=18,
            command=self.save_fig,
        )

        self.xscale_log = ctk.BooleanVar(value=False)
        self.yscale_log = ctk.BooleanVar(value=False)

        checkbox_xscale = ctk.CTkCheckBox(
            canvas_checkbox,
            variable=self.xscale_log,
            text="x log scale",
            checkbox_width=22,
            checkbox_height=18,
            border_width=2,
            command=self.update_canvas_scale,
        )
        checkbox_yscale = ctk.CTkCheckBox(
            canvas_checkbox,
            variable=self.yscale_log,
            text="y log scale",
            checkbox_width=22,
            checkbox_height=18,
            border_width=2,
            command=self.update_canvas_scale,
        )

        canvas_options.pack(fill="x", padx=5, pady=5)
        canvas_options.grid_columnconfigure((0, 1), weight=1)

        canvas_checkbox.grid(column=0, row=0, sticky="w")
        checkbox_xscale.pack(side=ctk.LEFT)
        checkbox_yscale.pack(side=ctk.LEFT, padx=10)
        save_fig_button.grid(column=1, row=0, sticky="e")

    def create_manager(self) -> None:
        manager_container = ctk.CTkFrame(self.container, fg_color="transparent")
        manager_container.grid(column=0, row=1, sticky="we", padx=100)

        manager_grid_container = ctk.CTkFrame(manager_container)
        manager_grid_container.pack(expand=True, fill="both")

        manager_grid_container.grid_rowconfigure(0, weight=1, uniform="mg_container")
        manager_grid_container.grid_rowconfigure(1, weight=2, uniform="mg_container")
        manager_grid_container.grid_columnconfigure(0, weight=1, uniform="mg_container")
        manager_grid_container.grid_columnconfigure(1, weight=1, uniform="mg_container")

        sample_selector_container = ctk.CTkFrame(
            manager_grid_container, fg_color="transparent"
        )
        sample_selector_container.grid(column=0, row=0, sticky="nwes")

        sample_selector_center = ctk.CTkFrame(
            sample_selector_container, fg_color="transparent"
        )
        sample_selector_center.pack(expand=True)

        sample_selector_label = ctk.CTkLabel(
            sample_selector_center, text="Experimental sample: "
        )
        self.sample_selector = ctk.CTkComboBox(
            sample_selector_center,
            width=80,
            values=[str(ind) for ind in range(1, self.db.nsamples + 1)],
            justify="center",
            command=lambda val: self.update_canvas(),
        )
        self.sample_selector.set("1")

        sample_selector_label.pack(side=ctk.LEFT, padx=5)
        self.sample_selector.pack(side=ctk.LEFT, padx=5)

        geometry_selector_container = ctk.CTkFrame(
            manager_grid_container, fg_color="transparent"
        )
        geometry_selector_container.grid(column=1, row=0, sticky="nwes")

        geometry_selector_center = ctk.CTkFrame(
            geometry_selector_container, fg_color="transparent"
        )
        geometry_selector_center.pack(expand=True)

        geometry_selector_label = ctk.CTkLabel(
            geometry_selector_center, text="Geometry: "
        )
        self.geometry_selector = ctk.CTkComboBox(
            geometry_selector_center,
            width=150,
            values=["Cylindrical", "Spherical", "Planar"],
            justify="center",
            command=lambda val: self.update_canvas(),
        )
        self.geometry_selector.set(config.read_entry("geometry"))

        geometry_selector_label.pack(side=ctk.LEFT, padx=5)
        self.geometry_selector.pack(side=ctk.LEFT, padx=5)

        mc_selector_container = ctk.CTkFrame(
            manager_grid_container, fg_color="transparent"
        )
        mc_selector_container.grid(column=2, row=0, sticky="nwes")

        mc_selector_center = ctk.CTkFrame(mc_selector_container, fg_color="transparent")
        mc_selector_center.pack(expand=True)

        self.mc_val = ctk.BooleanVar(value=self.db.mass_conservation)
        mc_selector_label = ctk.CTkLabel(mc_selector_center, text="Mass conservation: ")
        mc_selector = ctk.CTkCheckBox(
            mc_selector_center,
            variable=self.mc_val,
            text="",
            checkbox_width=22,
            checkbox_height=18,
            border_width=2,
            command=self.update_mc_selector,
        )

        mc_selector_label.pack(side=ctk.LEFT, padx=5)
        mc_selector.pack(side=ctk.LEFT, padx=5)

        slider_container = ctk.CTkFrame(manager_grid_container, fg_color="transparent")
        slider_container.grid(column=0, row=1, columnspan=3, sticky="nwes", pady=5)

        slider_container_center = ctk.CTkFrame(slider_container, fg_color="transparent")
        slider_container_center.pack(expand=True)

        self.slider: Dict[str, LabeledSlider] = {}
        for ind, key in enumerate(SLIDERS_CONFIG):
            labeled_slider = LabeledSlider(
                slider_container_center,
                text=SLIDERS_CONFIG[key]["text"],
                width=300,
                from_=0,
                to=len(self.tab[key]) - 1,
                command=lambda val: self.update_canvas(),
            )
            self.slider[key] = labeled_slider

            labeled_slider.label.grid(row=ind, column=0, padx=10, pady=5, sticky="w")
            labeled_slider.slider.grid(row=ind, column=1, padx=10, pady=5, sticky="e")

    def update_mc_selector(self):
        if self.mc_val.get():
            self.slider["clength"].label.grid_remove()
            self.slider["clength"].slider.grid_remove()
        else:
            self.slider["clength"].label.grid()
            self.slider["clength"].slider.grid()

    def update_canvas(self):
        sample = int(self.sample_selector.get())
        config.add_entry("sample", sample)

        t_ind, d_ind, clength_ind = self.get_current_indexes()

        x_exp, y_exp = self.db.get_experimental_sample(sample)
        egrid, signal = self.db.get_synthetic_signal(
            sample, t_ind, d_ind, clength_ind, self.geometry_selector.get()
        )

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

            if attr == "clength":
                attr_val = self.db.clength

            sym, unit, fmt = (
                SLIDERS_CONFIG[attr]["tex_symbol"],
                SLIDERS_CONFIG[attr]["unit"],
                SLIDERS_CONFIG[attr]["fmt"],
            )
            fmt = f"{attr_val:.2f}" if attr == "t_elec" else f"{attr_val:.2e}"

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
