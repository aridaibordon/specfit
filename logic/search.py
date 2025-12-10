import itertools

import numpy as np

from logic.database import SpecFitDatabase


def get_chi2(x, y, x_sample, y_sample):
    y = np.interp(x_sample, x, y)
    a = np.sum(y * y_sample) / np.sum(y**2)
    return sum((y_sample - a * y) ** 2 / (a * y))


def get_chi2_surface(sample: int, db: SpecFitDatabase):
    x_exp, y_exp = db.get_experimental_sample(sample, mode="search")

    chi2_surface = np.empty(
        shape=(
            len(db.tab_tev),
            len(db.tab_dne),
            len(db.tab_clength),
        )
    )
    for (t_ind, t_elec), (d_ind, d_elec), (clength_ind, clength) in itertools.product(
        enumerate(db.tab_tev), enumerate(db.tab_dne), enumerate(db.tab_clength)
    ):
        x, y = db.get_synthetic_signal(sample, t_ind, d_ind, clength_ind)
        chi2_surface[t_ind][d_ind][clength_ind] = get_chi2(x, y, x_exp, y_exp)

    return chi2_surface
