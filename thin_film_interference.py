import matplotlib.pyplot as plt
import numpy as np

ref = r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-13_22-32-43"
dark = r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-13_22-24-25"
spec = r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-13_22-29-06"

with open(spec+ "\spectrum_wavelengths.txt", "r") as f:
    wavelengths = [float(line.strip()) for line in f.readlines()]
ref_s = np.load(ref + r"\spectrum2D.npy")
dark_s = np.load(dark + r"\spectrum2D.npy")
spec_s = np.load(spec + r"\spectrum2D.npy")

YCENTER = 895
YBINS = 15

reflectance = (spec_s - dark_s)/(ref_s - dark_s)

plt.imshow(reflectance[(YCENTER-YBINS):(YCENTER+YBINS),:], aspect="auto", vmin=0, vmax=3)
plt.figure()
plt.plot(wavelengths, reflectance[(YCENTER-YBINS):(YCENTER+YBINS),:].sum(axis=0))
plt.ylim(-1,40)