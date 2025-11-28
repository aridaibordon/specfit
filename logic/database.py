import tomllib

from pathlib import Path

import numpy as np


class DatabaseReader_ABAKO:
    def __init__(self, db_path: str):
        self.path = Path(db_path)

        self.tab_tev = np.loadtxt(self.path / "tab_tev.txt")
        self.tab_dne = np.loadtxt(self.path / "tab_dne.txt")

    def get_info(self) -> dict:
        with open(self.path / "database.toml", "rb") as f:
            return tomllib.load(f)

    def get_radiative_properties(t_elec: float, d_elec: float):
        pass
