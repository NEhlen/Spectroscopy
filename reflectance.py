import matplotlib.pyplot as plt
import numpy as np

# ref_data = r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-12_20-31-09"
# spec_list = [
#     r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-12_21-02-42",
#     r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-12_20-43-43",
#     r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-12_20-39-22",
#     r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-12_20-34-58"
# ]
# spec_names = ["green_tight", "green_lose", "pink_lose", "yellow_tight"]

ref_data = r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-13_23-51-12"
spec_list = [r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-13_23-53-30"]
dark_data= r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-13_23-33-12"

spec_names = ["leaf"]

for spec_data in spec_list:
    with open(spec_data + "\spectrum_wavelengths.txt", "r") as f:
        wavelengths = [float(line.strip()) for line in f.readlines()]

    ref_spectrum = np.load(ref_data + "\spectrum2D.npy")
    real_spectrum = np.load(spec_data + "\spectrum2D.npy")
    dark_spectrum = np.load(dark_data + "\spectrum2D.npy")
    # real_spectrum -= dark_spectrum
    # ref_spectrum -= dark_spectrum
    reflectance = real_spectrum[875:905,:].sum(axis=0) / ref_spectrum[875:905,:].sum(axis=0)

    plt.figure(dpi=300)
    plt.plot(wavelengths, reflectance)
    plt.ylim(0, 5)

    plt.xlabel("wavelength [nm]")
    plt.ylabel("Reflectance")
plt.savefig("reflectance_test25.png")
