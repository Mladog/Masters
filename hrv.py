"""
Module responsible for signal analisys
"""

import numpy as np
from hrvanalysis import get_time_domain_features, get_poincare_plot_features, get_frequency_domain_features
from statsmodels.tsa.stattools import adfuller

def count_hrv(examination):
    """
    funkcja zwracająca parametry hrv w dziedzinie czasu, częstotliwości oraz nieliniowe
    """
    print(adfuller(examination.RR)[1])
    hrv_params = {"stationarity": False if adfuller(examination.RR)[1] > 0.05 else True,
                  "hrv_time": get_time_domain_features(examination.RR, False),
                  "hrv_nonlinear": get_poincare_plot_features(examination.RR),
                  "hrv_freq": get_frequency_domain_features(examination.RR, method="lomb")
                }
    return hrv_params

def create_hrv_summary(hrv_params):
    hrv_time = hrv_params["hrv_time"]
    hrv_freq = hrv_params["hrv_freq"]
    hrv_nonlinear = hrv_params["hrv_nonlinear"]
    text = f"""
        HRV w dziedzinie czasu:
        mean_nni: {np.round(hrv_time['mean_nni'], 3)}
        sdsd: {np.round(hrv_time['sdsd'], 3)}
        sdnn: {np.round(hrv_time['sdnn'], 3)}
        rmssd: {np.round(hrv_time['rmssd'], 3)}
        cvsd: {np.round(hrv_time['cvsd'], 3)}

        HRV w dziedzinie częstotliwości:
        hf: {np.round(hrv_freq['hf'],5)}
        lf: {np.round(hrv_freq['lf'],5)}
        vlf: {np.round(hrv_freq['vlf'],5)}
        lf/hf: {np.round(hrv_freq['lf_hf_ratio'],5)}
        total power: {np.round(hrv_freq['total_power'],5)}

        HRV nieliniowe:
        SD1: {np.round(hrv_nonlinear['sd1'], 3)}
        SD2: {np.round(hrv_nonlinear['sd2'], 3)}
        """
    return text