"""
Module responsible for signal analisys
"""

import numpy as np
from hrvanalysis import get_time_domain_features, get_poincare_plot_features, get_frequency_domain_features
from statsmodels.tsa.stattools import adfuller
import pyqtgraph as pg

def count_hrv(obj):
    """
    funkcja zwracająca parametry hrv w dziedzinie czasu, częstotliwości oraz nieliniowe
    """
    
    if obj.h1.isChecked() == True:
        obj.exam_start=0
        obj.exam_stop=len(obj.examination.RR)-1
        obj.hrv_range.clear()
    else:
        try:
            obj.exam_start=int(obj.textbox_start.text())
        except:
            obj.exam_start=0
            obj.textbox_start.setText("0")
        try:
            obj.exam_stop=int(obj.textbox_end.text())
            if obj.exam_stop <= obj.exam_start:
                obj.exam_stop = str(len(obj.examination.RR)-1)
                obj.textbox_end.setText(str(len(obj.examination.RR)-1))
        except:
            obj.exam_stop=len(obj.examination.RR)-1
            obj.textbox_end.setText(str(len(obj.examination.RR)-1))
        # narysowanie granic przedziału
        obj.hrv_range.clear()
        obj.hrv_range.addItem(pg.InfiniteLine(obj.exam_start, pen='r'))
        obj.hrv_range.addItem(pg.InfiniteLine(obj.exam_stop, pen='r'))
    stationarity_result = adfuller(obj.examination.RR[obj.exam_start:obj.exam_stop])[1]
    hrv_params = {"stationarity": stationarity_result,
                  "hrv_time": get_time_domain_features(obj.examination.RR[obj.exam_start:obj.exam_stop],False),
                  "hrv_nonlinear": get_poincare_plot_features(obj.examination.RR[obj.exam_start:obj.exam_stop]),
                  "hrv_freq": get_frequency_domain_features(obj.examination.RR[obj.exam_start:obj.exam_stop], method="lomb")
                }
    return hrv_params

def create_hrv_summary(hrv_params):
    if hrv_params["stationarity"] <= 0.05:
        stationarity_text = f"sygnał stacjonarny (p-wartość {round(hrv_params['stationarity'], 3)} dla testu adfuller)"
    else:
        stationarity_text = f"Uwaga, badanie niestacjonarne \n(p-wartość test adfuller: {round(hrv_params['stationarity'], 3)})\n"
    hrv_time = hrv_params["hrv_time"]
    hrv_freq = hrv_params["hrv_freq"]
    hrv_nonlinear = hrv_params["hrv_nonlinear"]
    text = f"""{stationarity_text}
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