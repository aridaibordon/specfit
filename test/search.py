import customtkinter as ctk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ui.components import TitledFrame


class TestSearchFrame(TitledFrame):
    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent, title="Searching tools for plasma characterization")

        self.container.grid_columnconfigure(0, weight=1, uniform="search_frame")
        self.container.grid_columnconfigure(1, weight=1, uniform="search_frame")
        self.container.grid_rowconfigure(0, weight=1, uniform="search_frame")
        self.container.grid_rowconfigure(1, weight=1, uniform="search_frame")

        self.create_figures()
        self.create_manager()
        self.create_canvas_layout()

    def create_figures(self) -> None:
        self.fig_chi2, ax_chi2 = plt.subplots(figsize=(6, 6), tight_layout=True)

        ax_chi2.set_xlabel("Electron density (cm$^{{-3}}$)")
        ax_chi2.set_ylabel("Electron temperature (eV)")

        self.fig_t_elec, ax_t_elec = plt.subplots(figsize=(6, 6), tight_layout=True)
        self.label_t_elec = ax_t_elec.text(
            0.50,
            1.02,
            s="best fit: $T_e$",
            transform=ax_t_elec.transAxes,
            ha="center",
            va="bottom",
        )

        ax_t_elec.set_xlabel("Electron temperature (eV)")
        ax_t_elec.set_ylabel("Probability density")

        self.fig_d_elec, ax_d_elec = plt.subplots(figsize=(6, 6), tight_layout=True)
        self.label_d_elec = ax_d_elec.text(
            0.50,
            1.02,
            s="best fit: $n_e$",
            transform=ax_d_elec.transAxes,
            ha="center",
            va="bottom",
        )

        ax_d_elec.set_xlabel("Electron temperature (eV)")
        ax_d_elec.set_ylabel("Probability density")

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
            values=["Sample 1", "Sample 2", "Sample 3"],
            justify="center",
            command=lambda val: self.update_canvas(),
        )
        self.sample_selector.set("Sample 1")

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
            manager_container_center, text="Start exhaustive search"
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
        pass
