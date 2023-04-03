"""
Module responsible for signal analisys
"""

import neurokit2 as nk
import numpy as np

def count_hrv(examination):
    """
    funkcja zwracająca parametry hrv w dziedzinie czasu, częstotliwości oraz nieliniowe
    """
    hrv_params = {"hrv_time": nk.hrv_time(examination.RR_vect, sampling_rate=1000, show=False),
                  "hrv_nonlinear": nk.hrv_nonlinear(examination.RR_vect, sampling_rate=1000, show=False),
                  "hrv_freq": nk.hrv_frequency({"RRI": examination.RR}, 
                              sampling_rate=1000,
                              psd_method='welch',
                              show=False,
                              normalize=True,
                              order_criteria=None,
                              interpolation_rate=100)}
    return hrv_params

def create_hrv_summary(hrv_params):
    hrv_time = hrv_params["hrv_time"]
    hrv_freq = hrv_params["hrv_freq"]
    hrv_nonlinear = hrv_params["hrv_nonlinear"]
    text = f"""
        HRV w dziedzinie czasu:
        sdsd: {np.round(hrv_time.HRV_SDSD[0], 3)}
        sdnn: {np.round(hrv_time.HRV_SDNN[0], 3)}
        rmssd: {np.round(hrv_time.HRV_RMSSD[0], 3)}
        cvsd: {np.round(hrv_time.HRV_CVSD[0], 3)}

        HRV w dziedzinie częstotliwości:
        hf: {np.round(hrv_freq.HRV_HF[0],5)}
        lf: {np.round(hrv_freq.HRV_LF[0],5)}
        vlf: {np.round(hrv_freq.HRV_VLF[0],5)}
        lf/hf: {np.round(hrv_freq.HRV_LFHF[0],5)}

        HRV nieliniowe:
        SD1: {np.round(hrv_nonlinear.HRV_SD1[0], 3)}
        SD2: {np.round(hrv_nonlinear.HRV_SD2[0], 3)}
        """
    return text