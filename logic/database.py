import tomllib

from pathlib import Path
from typing import Dict

import numpy as np

from numpy.typing import NDArray

from logic.chi2_search import get_chi2_scale_factor


class SpecFitDatabase:
    def __init__(self, db_path: str):
        self.path = Path(db_path)

        self.tab_tev = np.loadtxt(self.path / "tab_tev.txt")
        self.tab_dne = np.loadtxt(self.path / "tab_dne.txt")
        self.tab_clength = np.loadtxt(self.path / "tab_clength.txt")

        db_info = self.get_info()
        self.code = db_info["synthetic"]["code"]
        self.mass_conservation = db_info["synthetic"]["mass_conservation"]

        self.nsamples = db_info["lineout"]["nsamples"]

    def get_nsamples(self) -> int:
        return len(self)

    def get_info(self) -> dict:
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
                self.path / "database" / f"rad_{t_ind+1:03d}_{d_ind+1:03d}.txt"
            ).T

            return egrid, j_bb, j_bf, j_ff, k_bb, k_bf, k_ff

        return np.loadtxt(
            self.path / "database" / f"rad_{t_ind+1:03d}_{d_ind+1:03d}.txt"
        ).T

    def get_synthetic_signal(
        self,
        sample: int,
        t_ind: int,
        d_ind: int,
        clenght_ind: int,
        geometry: str = "S",
    ):
        egrid, j_bb, j_bf, j_ff, k_bb, k_bf, k_ff = self.get_radiative_properties(
            t_ind, d_ind
        )
        clength = self.tab_clength[clenght_ind]

        k = k_bb + k_bf + k_ff
        if geometry == "P":
            signal = (j_bb + j_bf) / k * (1 - np.exp(-clength * k))
        elif geometry == "S":
            signal = (
                np.pi
                * clength**2
                * ((j_bb + j_bf) / k)
                * (
                    1
                    + np.exp(-2 * k * clength) / (k * clength)
                    - (1 - np.exp(-2 * k * clength)) / (2 * (k * clength) ** 2)
                )
            )

        x_exp, y_exp = self.get_experimental_sample(sample)
        signal *= get_chi2_scale_factor(egrid, signal, x_exp, y_exp)

        return egrid, signal

    def get_experimental_sample(self, sample: int):
        return np.loadtxt(self.path / "lineout" / f"s{sample}.txt").T
