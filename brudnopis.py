"""
Module responsible for signal analisys
"""

# %%
from examination import Examination
from hrv import count_hrv

ex = Examination("C:/Users/mlado/Desktop/Masters/data/RR_YoYo.csv")
hrv = count_hrv(ex)
# %%
