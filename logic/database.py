import tomllib

from pathlib import Path
from typing import Tuple

import numpy as np

from numpy.typing import NDArray


class DatabaseReader_ABAKO:
    def __init__(self, db_path: str):
        self.path = Path(db_path)

        self.tab_tev = np.loadtxt(self.path / "tab_tev.txt")
        self.tab_dne = np.loadtxt(self.path / "tab_dne.txt")
        self.tab_clength = np.loadtxt(self.path / "tab_clength.txt")

    def get_info(self) -> dict:
        with open(self.path / "database.toml", "rb") as f:
            return tomllib.load(f)

    def get_data_tables(self) -> Tuple[NDArray, NDArray]:
        return self.tab_tev, self.tab_dne

    def get_radiative_properties_from_ind(self, t_ind: int, d_ind: int, clength_ind):
        fname = self.path / "database" / f"rad_{t_ind}_{d_ind}.txt"
        ...
