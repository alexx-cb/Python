import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import h5py

"""
DATASET DE LA NASA

Deep Space Climate Observatory National Institute of Standards and Technology Advanced Radiometer Level 1B Radiance Filtered, Version 3

Medida continua de como La Tierra refleja/emite energia en diferentes longitudes de onda
"""

file_path = "Files/nist_1b_202501_filtered_03.h5"

def cargar_banda(file_path, band_path, include_lunar=False):
    with h5py.File(file_path, "r") as f:
        dset = f[band_path]

        time = np.array(dset["DSCOVREpochTime"][:], dtype=np.float64)

        radiance = dset["EarthRadiance"][:]
        radiance = radiance.byteswap().view(radiance.dtype.newbyteorder("="))

        interp = np.array(dset["isInterpolated"][:])

        data = {
            "Time": time,
            "Radiance": radiance,
            "Is_interpolated": interp
        }

        if include_lunar:
            lunar = dset["LunarCorrection"][:]
            data["LunarCorrection"] = lunar

        return pd.DataFrame(data)



df_bandA = cargar_banda(file_path, "Earth_Radiance_Filtered/Band A (Total)")
df_bandB = cargar_banda(file_path, "Earth_Radiance_Filtered/Band B (Shortwave)", include_lunar=True)
df_bandC = cargar_banda(file_path, "Earth_Radiance_Filtered/Band C (NIR)")


print(pd.to_datetime(df_bandB["Time"], unit="s").min())
print(pd.to_datetime(df_bandB["Time"], unit="s").max())

