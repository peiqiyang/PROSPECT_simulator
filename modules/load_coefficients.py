
import numpy as np

def load_coefficients(base_path="data/"):
    wl = np.loadtxt(base_path + "wavelengths.txt")
    nr = np.loadtxt(base_path + "nr.txt")
    Kab = np.loadtxt(base_path + "Kab.txt")
    Kcar = np.loadtxt(base_path + "Kcar.txt")
    Kw = np.loadtxt(base_path + "Kw.txt")
    Km = np.loadtxt(base_path + "Km.txt")
    return wl, nr, Kab, Kcar, Kw, Km
