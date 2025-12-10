import importlib.util
import tomllib

from pathlib import Path
from typing import Dict, Literal

import numpy as np

from numpy.typing import NDArray

import config

from logic.post import apply_instrument_resolution


def load_database(db_path: str):
    return SpecFitDatabase(db_path)


def get_chi2_scale_factor(x, y, x_sample, y_sample):
    y = np.interp(x_sample, x, y)
    return np.sum(y * y_sample) / np.sum(y**2)


def import_database_specific_module(fpath: str):
    spec = importlib.util.spec_from_file_location("dynamic_module", fpath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SpecFitDatabase:
    def __init__(self, db_path: str):
        self.path = Path(db_path)

        self.config = self.get_database_configuration()
        if (self.path / "database.py").exists():
            self.module = import_database_specific_module(self.path / "database.py")

        self.code = self.config["synthetic"]["code"]
        self.mass_conservation = self.config["synthetic"]["mass_conservation"]

        self.tab_tev = np.loadtxt(self.path / "tab_tev.txt", skiprows=0)
        self.tab_dne = np.loadtxt(self.path / "tab_dne.txt", skiprows=0)
        self.tab_clength = np.loadtxt(self.path / "tab_clength.txt", skiprows=0)

        self.nsamples = self.config["lineout"]["nsamples"]

    def get_nsamples(self) -> int:
        return len(self)

    def get_database_configuration(self) -> dict:
        with open(self.path / "database.toml", "rb") as f:
            return tomllib.load(f)

    def get_data_tables(self) -> Dict[str, NDArray]:
        return {
            "t_elec": self.tab_tev,
            "d_elec": self.tab_dne,
            "clength": self.tab_clength,
        }

    def get_radiative_properties(self, t_ind: int, d_ind: int):
        if self.code == "ABAKO":
            egrid, j_bb, j_bf, j_ff, _, k_bb, k_bf, k_ff, _, _, _ = np.loadtxt(
                self.path / "database" / f"rad_{t_ind + 1:03d}_{d_ind + 1:03d}.txt"
            ).T

            return egrid, j_bb, j_bf, j_ff, k_bb, k_bf, k_ff

        return np.loadtxt(
            self.path / "database" / f"rad_{t_ind + 1:03d}_{d_ind + 1:03d}.txt"
        ).T

    def get_clength(self, t_ind, d_ind, clength_ind):
        t_elec, d_elec = self.tab_tev[t_ind], self.tab_dne[d_ind]

        if self.mass_conservation:
            clength = self.module.get_clength(t_elec, d_elec)
        else:
            clength = self.tab_clength[clength_ind]

        return clength

    def get_synthetic_signal(
        self,
        sample: int,
        t_ind: int,
        d_ind: int,
        clength_ind: int,
        geometry: Literal["Cylindrical", "Spherical", "Planar"] = "Spherical",
    ):
        egrid, j_bb, j_bf, j_ff, k_bb, k_bf, k_ff = self.get_radiative_properties(
            t_ind, d_ind
        )

        self.clength = self.get_clength(t_ind, d_ind, clength_ind)

        k = k_bb + k_bf + k_ff
        if geometry == "Planar":
            signal = (j_bb + j_bf) / k * (1 - np.exp(-self.clength * k))
        elif geometry == "Spherical" or geometry == "Cylindrical":
            signal = (
                np.pi
                * self.clength**2
                * ((j_bb + j_bf) / k)
                * (
                    1
                    + np.exp(-2 * k * self.clength) / (k * self.clength)
                    - (1 - np.exp(-2 * k * self.clength))
                    / (2 * (k * self.clength) ** 2)
                )
            )

        delta_E = self.config["synthetic"]["post"]["resolution"]
        signal = apply_instrument_resolution(egrid, signal, delta_E)

        x_chi2, y_chi2 = self.get_experimental_sample(sample, mode="search")
        signal *= get_chi2_scale_factor(egrid, signal, x_chi2, y_chi2)

        post_chi2 = self.config["synthetic"].get("post_chi2")
        if post_chi2:
            my_config = config.load()
            for func_name in post_chi2:
                func = getattr(self.module, func_name)
                egrid, signal = func(egrid, signal, my_config)

        min_e, max_e = self.config["lineout"].get("photon_range")
        mask = (egrid > min_e) & (egrid < max_e)

        return egrid[mask], signal[mask]

    def get_experimental_sample(
        self,
        sample: int,
        mode: Literal["fit", "search"] = "fit",
    ):
        egrid, signal = np.loadtxt(self.path / "lineout" / f"s{sample}.txt").T

        if mode == "fit":
            min_e, max_e = self.config["lineout"].get("photon_range")
            mask = (egrid > min_e) & (egrid < max_e)

            return egrid[mask], signal[mask]

        elif mode == "search":
            selected_range = self.config["lineout"].get("chi2_range")

            selected_energies = []
            selected_lines = []
            for emin, emax in selected_range:
                mask = (egrid > emin) & (egrid < emax)
                selected_energies.extend(egrid[mask])
                selected_lines.extend(signal[mask])

            return selected_energies, selected_lines
