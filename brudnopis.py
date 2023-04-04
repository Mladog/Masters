"""
Module responsible for signal analisys
"""

# %%
from examination import Examination
from hrv import count_hrv
import matplotlib.pyplot as plt
import numpy as np

def find_art1(RR):
    d_prev = [1 if abs(d) > 20 else 0 for d in ex.RR[1:]- ex.RR[:-1]]
    d_prev.insert(0, 0)

    d_next = [1 if abs(d) > 20 else 0 for d in ex.RR[:-1]-ex.RR[1:]]
    d_next.insert(-1, 0)

    final_list = [sum(value) for value in zip(prev, d_next)]
    idx = np.where(np.array(final_list) == 2)[0]

    return idx

# %%
ex = Examination("C:/Users/mlado/Desktop/Masters/data/RR_YoYo.csv")
hrv = count_hrv(ex)

idx = find_art1(ex.RR)
plt.plot(ex.RR)
plt.plot(idx, ex.RR[idx], 'ro')



# %%
