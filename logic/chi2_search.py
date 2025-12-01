import numpy as np


def get_chi2(x, y, x_sample, y_sample):
    y = np.interp(x_sample, x, y)
    a = np.sum(y * y_sample) / np.sum(y**2)
    return sum((y_sample - a * y) ** 2 / (a * y))


def get_chi2_scale_factor(x, y, x_sample, y_sample):
    y = np.interp(x_sample, x, y)
    return np.sum(y * y_sample) / np.sum(y**2)
