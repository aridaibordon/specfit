import numpy as np

import numpy as np

c = 2.99792458e10  # cm/s
h = 4.13566727e-15  # (h en eVs)


def normal_dist(x: list | float, mean: float, sigma: float):
    return 1 / np.sqrt(2 * np.pi * sigma**2) * np.exp(-0.5 * ((x - mean) / sigma) ** 2)


def apply_instrument_resolution(egrid, signal, delta_E: float):
    x = np.arange(-4 * delta_E, 4 * delta_E, egrid[1] - egrid[0])
    gaussian = normal_dist(x - np.mean(x), 0, delta_E / 2.355)

    return np.convolve(signal, gaussian, mode="same")

# def apply_instrument_resolution(egrid, signal, delta_lambda: float):
#     # convert spectral axis to nm
#     lgrid = h * c / egrid * 1e7
#     lsignal = h * c / lgrid**2 * signal
# 
#     # linearize lambda grid and signal
#     lgrid_aux = np.linspace(min(lgrid), max(lgrid), len(lgrid))
#     lsignal_aux = np.interp(lgrid_aux, lgrid[::-1], lsignal[::-1])
# 
#     # apply instrumental resolution in lambda
#     signal_conv = np.convolve(
#         lsignal_aux,
#         normal_dist(lgrid_aux - np.mean(lgrid_aux), 0, delta_lambda / 2.355),
#         mode="same",
#     )
# 
#     # reconvert spectral axis to eV
#     egrid_aux = h * c / lgrid_aux * 1e7
#     esignal_aux = h * c / egrid_aux**2 * signal_conv
# 
#     # return signal in original egrid axis
#     return np.interp(egrid, egrid_aux[::-1], esignal_aux[::-1])
