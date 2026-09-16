import logging

from pathlib import Path

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config

from logic.database import load_database
from logic.search import get_chi2_surface
from ui.components import TitledFrame


class SearchFrame(TitledFrame):
    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent, title="Searching tools for plasma characterization")

        self.db = load_database(db_path=config.read_entry("db"))
        self.tab = self.db.get_data_tables()

        self.container.grid_columnconfigure(0, weight=1, uniform="search_frame")
        self.container.grid_columnconfigure(1, weight=1, uniform="search_frame")
        self.container.grid_rowconfigure(0, weight=1, uniform="search_frame")
        self.container.grid_rowconfigure(1, weight=1, uniform="search_frame")

        self.load_chi2_surface()

        self.create_figures()
        self.create_manager()
        self.create_canvas_layout()

    def create_figures(self) -> None:
        prob = np.exp(-self.nchi2_surface[:, :, 2])

        t_elec_prob = np.sum(prob, axis=1)
        d_elec_prob = np.sum(prob, axis=0)

        # chi2-surface plot
        self.fig_chi2, ax_chi2 = plt.subplots(tight_layout=True)

        ax_chi2.pcolormesh(
            self.db.tab_dne, self.db.tab_tev / 1e3, prob, shading="gouraud"
        )

        ax_chi2.set_xlabel("Electron density (cm$^{-3}$)")
        ax_chi2.set_ylabel("Electron temperature (keV)")

        ax_chi2.set_xscale("log")

        # best fit
        best_t_ind, best_d_ind = np.where(prob == np.max(prob))
        best_t_elec, best_d_elec = (
            self.db.tab_tev[best_t_ind][0],
            self.db.tab_dne[best_d_ind][0],
        )

        # confidence interval
        ci_t_elec_threshold = np.max(t_elec_prob) / np.e**0.5
        ci_t_elec_values = self.db.tab_tev[t_elec_prob > ci_t_elec_threshold]
        ci_t_elec_range = [np.min(ci_t_elec_values), np.max(ci_t_elec_values)]
        ci_t_elec_lower, ci_t_elec_upper = ci_t_elec_range

        ci_d_elec_threshold = np.max(d_elec_prob) / np.e**0.5
        ci_d_elec_values = self.db.tab_dne[d_elec_prob > ci_d_elec_threshold]
        ci_d_elec_range = [min(ci_d_elec_values), max(ci_d_elec_values)]
        ci_d_elec_lower, ci_d_elec_upper = ci_d_elec_range

        # electron temperature plot
        self.fig_t_elec, ax_t_elec = plt.subplots(tight_layout=True)

        ax_t_elec.plot(self.db.tab_tev / 1e3, t_elec_prob)
        ax_t_elec.text(
            0.5,
            1.02,
            s=f"best fit: $T_e = {best_t_elec / 1e3:.2f}\,^{{+{np.abs(best_t_elec - ci_t_elec_upper) / 1e3:.2f}}}_{{-{np.abs(best_t_elec - ci_t_elec_lower) / 1e3:.2f}}}$ keV",
            transform=ax_t_elec.transAxes,
            ha="center",
            va="bottom",
        )

        ax_t_elec.set_xlabel("Electron temperature (keV)")
        ax_t_elec.set_ylabel("Probability density")

        # electron density plot
        self.fig_d_elec, ax_d_elec = plt.subplots(tight_layout=True)

        ax_d_elec.plot(self.db.tab_dne, d_elec_prob)
        ax_d_elec.text(
            0.5,
            1.02,
            s=f"best fit: $n_e = ${best_d_elec:.2e}$\,^{{+{np.abs(best_d_elec - ci_d_elec_upper):.2e}}}_{{-{np.abs(best_d_elec - ci_d_elec_lower):.2e}}}$ cm$^{{-3}}$",
            transform=ax_d_elec.transAxes,
            ha="center",
            va="bottom",
        )

        ax_d_elec.set_xlabel("Electron density (cm$^{-3}$)")
        ax_d_elec.set_ylabel("Probability density")

        ax_d_elec.set_xscale("log")

    def create_manager(self):
        manager_container = ctk.CTkFrame(self.container, fg_color="transparent")
        manager_container.grid(column=0, row=0, sticky="nwes", padx=5, pady=5)

        manager_container_center = ctk.CTkFrame(manager_container)
        manager_container_center.pack(expand=True)

        sample_selector_label = ctk.CTkLabel(
            manager_container_center, text="Experimental sample: "
        )
        self.sample_selector = ctk.CTkComboBox(
            manager_container_center,
            width=200,
            values=[str(ind) for ind in range(1, self.db.nsamples + 1)],
            justify="center",
            command=lambda val: self.update_canvas(),
        )
        self.sample_selector.set("1")

        sample_selector_label.grid(column=0, row=0, sticky="w", padx=5, pady=5)
        self.sample_selector.grid(column=1, row=0, padx=5, pady=5)

        fom_selector_label = ctk.CTkLabel(
            manager_container_center, text="Figure-of-merit: "
        )
        self.fom_selector = ctk.CTkComboBox(
            manager_container_center,
            width=200,
            values=["Chi-square", "Chi-square (log)"],
            justify="center",
            command=lambda val: self.update_canvas(),
        )
        self.fom_selector.set("Chi-square")

        fom_selector_label.grid(column=0, row=1, sticky="w", padx=5, pady=5)
        self.fom_selector.grid(column=1, row=1, padx=5, pady=5)

        search_button = ctk.CTkButton(
            manager_container_center,
            text="Start exhaustive search",
            command=self.start_exhaustive_search,
        )
        search_button.grid(column=0, row=2, columnspan=2, pady=10, ipadx=10)

    def create_canvas_layout(self):
        self.canvas1 = FigureCanvasTkAgg(self.fig_chi2, self.container)
        self.canvas1.get_tk_widget().grid(
            column=1, row=0, sticky="nwes", padx=5, pady=5
        )

        self.canvas2 = FigureCanvasTkAgg(self.fig_t_elec, self.container)
        self.canvas2.get_tk_widget().grid(
            column=0, row=1, sticky="nwes", padx=5, pady=5
        )

        self.canvas3 = FigureCanvasTkAgg(self.fig_d_elec, self.container)
        self.canvas3.get_tk_widget().grid(
            column=1, row=1, sticky="nwes", padx=5, pady=5
        )

    def update_canvas(self):
        sample = int(self.sample_selector.get())
        config.add_entry("sample", sample)

    def start_exhaustive_search(self):
        sample = config.read_entry("sample")
        fpath = Path(self.db.path / "lineout" / f"s{sample}_chi2.npy")

        logging.info("Computing chi2 surface. This may take some time ...")
        chi2_surface = get_chi2_surface(sample, self.db)
        np.save(fpath, chi2_surface)

        self.nchi2_surface = chi2_surface / np.min(chi2_surface)

        self.update_canvas()

    def load_chi2_surface(self):
        sample = config.read_entry("sample")
        fpath = Path(self.db.path / "lineout" / f"s{sample}_chi2.npy")
        if Path(fpath).exists():
            chi2_surface = np.load(fpath)
        else:
            logging.info("Computing chi2 surface. This may take some time ...")
            chi2_surface = get_chi2_surface(sample, self.db)
            np.save(fpath, chi2_surface)

        self.nchi2_surface = chi2_surface / np.min(chi2_surface)
