# %%
"""
Module responsible for signal analisys
"""

from hrvanalysis import get_time_domain_features, get_frequency_domain_features, get_poincare_plot_features
from examination import Examination
from hrv import count_hrv
import matplotlib.pyplot as plt
import numpy as np

ex = Examination("C:/Users/mlado/Desktop/Masters/data/RRy z Yo-Yo/21102002_Bondarczyk Filip.txt")
hrv = count_hrv(ex)

nonlin_domain_features = get_poincare_plot_features(ex.RR)

# %%
