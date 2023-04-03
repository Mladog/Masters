"""
Module responsible for signal analisys
"""
# %%
import neurokit2 as nk
import numpy as np

fname = "C:/Users/mlado/Desktop/Masters/data/RR_YoYo.csv"
examination = np.genfromtxt(fname, delimiter=",")
examination= examination.astype(int)

#policzenie sumy do wyznaczenia czasu
time = np.sum(examination) # wyrażony w ms
peak_vect = np.zeros(int(time))
np.put(peak_vect, examination, 1)
# %%

# Drop all columns with NaN values
hrv_indices_clean=hrv_indices.dropna(axis=1)
# %%

# %%
hrv_indices = nk.hrv(peak_vect, sampling_rate=1000, show=True) # tak się szybciej liczy
hrv_freq = nk.hrv_frequency({"RRI": examination}, sampling_rate=1000, 
                            psd_method='welch', show=True, silent=False, normalize=False, order_criteria=None, interpolation_rate=100)

# %%
