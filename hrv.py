"""
Module responsible for signal analisys
"""

import numpy as np
from statsmodels.tsa.stattools import adfuller
from scipy.signal import lombscargle
import pyqtgraph as pg

def count_hrv(obj):
    """
    funkcja zwracająca parametry hrv w dziedzinie czasu, częstotliwości oraz nieliniowe
    """
    #print(adfuller(examination.RR)[1])
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

    hrv_params = {"stationarity": False if adfuller(obj.examination.RR[obj.exam_start:obj.exam_stop])[1] > 0.05 else True,
                  "hrv_time": time_domain(obj.examination.RR[obj.exam_start:obj.exam_stop]),
                  "hrv_nonlinear": non_linear(obj.examination.RR[obj.exam_start:obj.exam_stop])
                }
    return hrv_params

def create_hrv_summary(hrv_params):
    hrv_time = hrv_params["hrv_time"]
    #hrv_freq = hrv_params["hrv_freq"]
    hrv_nonlinear = hrv_params["hrv_nonlinear"]
    text = f"""
HRV w dziedzinie czasu:
mean_nni: {np.round(hrv_time['mrri'], 3)}
sdsd: {np.round(hrv_time['sdsd'], 3)}
sdnn: {np.round(hrv_time['sdnn'], 3)}
rmssd: {np.round(hrv_time['rmssd'], 3)}

HRV nieliniowe:
SD1: {np.round(hrv_nonlinear['sd1'], 3)}
SD2: {np.round(hrv_nonlinear['sd2'], 3)}
        """
    return text

def time_domain(RR):
    diff_rri = np.diff(RR)
    rmssd = np.sqrt(np.mean(diff_rri ** 2))
    sdnn = np.std(RR, ddof=1)  # make it calculates N-1
    sdsd = np.std(diff_rri, ddof=1)
    nn50 = _nn50(RR)
    pnn50 = _pnn50(RR)
    mrri = np.mean(RR)
    mhr = np.mean(60 / (RR / 1000.0))

    return dict(
        zip(
            ["rmssd", "sdnn", "sdsd", "nn50", "pnn50", "mrri", "mhr"],
            [rmssd, sdnn, sdsd, nn50, pnn50, mrri, mhr],
        )
    )


def _nn50(RR):
    return sum(abs(np.diff(RR)) > 50)


def _pnn50(RR):
    return _nn50(RR) / len(RR) * 100

def non_linear(RR):
    sd1, sd2 = _poincare(RR)
    return dict(zip(["sd1", "sd2"], [sd1, sd2]))

def _poincare(RR):
    diff_rri = np.diff(RR)
    sd1 = np.sqrt(np.std(diff_rri, ddof=1) ** 2 * 0.5)
    sd2 = np.sqrt(2 * np.std(RR, ddof=1) ** 2 - 0.5 * np.std(diff_rri, ddof=1) ** 2)
    return sd1, sd2

"""HRV w dziedzinie częstotliwości:
hf: {np.round(hrv_freq['hf'],5)}
lf: {np.round(hrv_freq['lf'],5)}
vlf: {np.round(hrv_freq['vlf'],5)}
lf/hf: {np.round(hrv_freq['lf_hf_ratio'],5)}
total power: {np.round(hrv_freq['total_power'],5)}"""