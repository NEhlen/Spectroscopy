import datetime as dt
import json

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

CUR_TIME = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
SPEC_FOLDER = r"C:\Users\Niels Ehlen\Documents\Programme\Spectroscopy\data\spectrum_2023-12-13_23-53-30"
CONFIGURATION_FILE = (
    SPEC_FOLDER + "\metadata.json"
)
SAVE_FILES = f"spectrum_{CUR_TIME}"

YBINS = 20
YCENTER = 895


# SPECTRUM DATA
with open(CONFIGURATION_FILE, "r") as f:
    configuration = json.load(f)

configuration["y_center"] = YCENTER
configuration["y_bins"] = YBINS

#picture = np.load(SPEC_FOLDER + r"\raw_data.npy")
picture_gray = np.load(SPEC_FOLDER + r"\raw_data_gray.npy")


# HELPER FUNCTIONS

def calibrate(calibration_spots: list, center_pixel: int = 1296.0):
    center = float(center_pixel)
    constants = []
    for cal in calibration_spots:
        c = (float(cal[0]) - center) / (
            np.tan(
                np.arcsin(cal[1] * 1e-6 / configuration["grid"])
                - configuration["center_angle"]
            )
        )
        constants.append(c)
    mean_c = np.mean(constants)
    return mean_c


# recalculate x-vals
def pix2wavelength(
    pix_list: np.ndarray,
    mean_const: float,
    center_pix: int = 1296.0,
):
    center = float(center_pix)

    return (
        configuration["grid"]
        * np.sin(
            np.arctan2(pix_list - center, mean_const) + configuration["center_angle"]
        )
        * 1e6
    )


# take picture
pixels = np.array(range(picture_gray.shape[1]))
# Interpolate Wavelength
mean_c = calibrate(
    [
        (1150, 612),
        (1550, 464),
        (813, 686.719),
        (427, 822.696),
        (599, 759.370)],  # pixels2wavelength
    int(picture_gray.shape[1] // 2),  # CHECK!!!
)
wavelengths = -pix2wavelength(
    pixels,
    mean_c,
    int(picture_gray.shape[1] // 2),  #  CHECK!!!
)

wav2pix = interpolate.interp1d(wavelengths, picture_gray, axis=1)
# interpolate image from pixels to wavelengths
linear_wavelengths = np.arange(880, 400, -0.5)
spectrum_grayscale = wav2pix(linear_wavelengths)
spectrum = spectrum_grayscale.copy()

# generate grayscale version of spectrum by weighting the red, green and blue components
# values taken from standard NTSC formula
# spectrum_grayscale = np.dot(
#     spectrum,
#     np.array([0.299, 0.587, 0.114]),
# )

savedir = SPEC_FOLDER + "/"
#os.makedirs(savedir, exist_ok=True)

# Write the array to disk
np.save(savedir + "spectrum2D.npy", spectrum_grayscale)

with open(savedir + "spectrum_wavelengths.txt", "w+") as f:
    f.writelines("\n".join([str(i) for i in linear_wavelengths]))


fig, ax = plt.subplots(1)
ax.imshow(
    spectrum,
    extent=[linear_wavelengths[0], linear_wavelengths[-1], 0, spectrum.shape[0]],
    aspect="auto",
    vmin=0,
    vmax=4 * spectrum.std(),
)
ax.set_xlabel("Wavelength [nm]")
fig.savefig(savedir + "spectrum.png")
fig.clf()
plt.close()

fig, ax = plt.subplots(1)
ax.imshow(
    spectrum_grayscale,
    extent=[linear_wavelengths[0], linear_wavelengths[-1], 0, spectrum.shape[0]],
    aspect="auto",
    vmin=0,
    vmax=3 * spectrum.std(),
)
ax.set_xlabel("Wavelength [nm]")
fig.savefig(savedir + "spectrum_gray.png")
fig.clf()
plt.close()

fig, ax = plt.subplots(1, dpi=300)
ax.plot(
    linear_wavelengths,
    spectrum_grayscale[YCENTER - YBINS : YCENTER + YBINS, :].mean(axis=0),
)
ax.set_xlabel("Wavelength [nm]")
ax.set_ylabel("Intensity [a.u.]")
fig.savefig(savedir + "spectrum_1d.png")
fig.clf()
plt.close()
