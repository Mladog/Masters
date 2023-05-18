"""
Module responsible for signal analisys
"""

import numpy as np
from hrvanalysis import get_time_domain_features, get_poincare_plot_features, get_frequency_domain_features
from statsmodels.tsa.stattools import adfuller
import pyqtgraph as pg
import scipy

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
                  "hrv_time": count_time_domain(obj.examination.RR[obj.exam_start:obj.exam_stop]),
                  "hrv_nonlinear": get_poincare_plot_features(obj.examination.RR[obj.exam_start:obj.exam_stop]),
                  "hrv_freq": count_freq_domain(obj.examination.RR[obj.exam_start:obj.exam_stop])
                }
    return hrv_params

def create_hrv_summary(hrv_params):
    if hrv_params["stationarity"] <= 0.05:
        stationarity_text = f"sygnał stacjonarny (p-wartość {round(hrv_params['stationarity'], 3)} dla testu adfuller)"
    else:
        stationarity_text = f"Uwaga, badanie niestacjonarne \n(p-wartość test adfuller: {round(hrv_params['stationarity'], 3)})\n"
    stationarity_text = ""
    hrv_time = hrv_params["hrv_time"]
    hrv_freq = hrv_params["hrv_freq"]
    hrv_nonlinear = hrv_params["hrv_nonlinear"]
    text = f"""{stationarity_text}
HRV w dziedzinie czasu:
średnia: {np.round(hrv_time['mean'], 3)}
SDNN: {np.round(hrv_time['sdnn'], 3)}
RMSSD: {np.round(hrv_time['rmssd'], 3)}
pnnx: {np.round(hrv_time['pnnx'], 3)}
triang: {np.round(hrv_time['triang'], 3)}
TINN: {np.round(hrv_time['tinn'], 3)}

HRV w dziedzinie częstotliwości:
hf: {np.round(hrv_freq['HFabs'],5)}
lf: {np.round(hrv_freq['LFabs'],5)}
lf nu: {np.round(hrv_freq['LFnu'],5)}
hf nu: {np.round(hrv_freq['HFnu'],5)}
vlf: {np.round(hrv_freq['VLFabs'],5)}
lf/hf: {np.round(hrv_freq['LFHF'],5)}

HRV nieliniowe:
SD1: {np.round(hrv_nonlinear['sd1'], 3)}
SD2: {np.round(hrv_nonlinear['sd2'], 3)}
        """
    return text

    results["VLFabs"] = np.median(vlfabs)
    results["LFabs"] = np.median(lfabs)
    results["HFabs"] = np.median(hfabs)
    results["LFnu"] = np.median(lfnu)
    results["HFnu"] = np.median(hfnu)
    results["LFHF"] = np.median(lfhf)

def count_freq_domain(RR):
    params = [3, [0.0, 0.04], [0.04, 0.15], [0.15, 0.4]]  # InterpRate, VLF, LF, HF
    vlfBand = [0.0, 0.04]
    lfBand = [0.04, 0.15]
    hfBand = [0.15, 0.4]
    interpRate = 3
    siginfo = []
    timeSig = np.cumsum(RR).tolist()
    seriesSig = RR
    #for timeSig, seriesSig in zip(timestamps, values):  # For each signal PAIR (time,signal)

    # Checking if time is in seconds
    medDiff = np.median([x - y for x, y in zip(timeSig[1:], timeSig[:-1])])
    if medDiff > 20:  # is in milliseconds
        timeSig = [t/1000 for t in timeSig]  # change to seconds

    # Interpolate series
    funcInterp = scipy.interpolate.interp1d(timeSig, seriesSig, 'cubic')
    newTime = np.arange(timeSig[0], timeSig[-1], 1 / interpRate)
    newSeries = funcInterp(newTime)

    vlfabs = []
    lfabs = []
    hfabs = []
    lfnu = []
    hfnu = []
    lfhf = []

    # segments is a list of series. If no segmentation is desired,
    # the only element is the original series

    f, psd = scipy.signal.periodogram(RR, interpRate, detrend=False)
    vlfRange = (vlfBand[0] <= f) * (f <= vlfBand[1])
    lfRange = (lfBand[0] <= f) * (f <= lfBand[1])
    hfRange = (hfBand[0] <= f) * (f <= hfBand[1])
    #print(f)
    #print(lfRange)
    #print(hfRange)
    freqResol = f[1]-f[0]
    vlfPower = np.sum(psd[vlfRange]) * freqResol
    lfPower = np.sum(psd[lfRange]) * freqResol
    hfPower = np.sum(psd[hfRange]) * freqResol
    vlfabs.append(vlfPower)
    lfabs.append(lfPower)
    hfabs.append(hfPower)
    lfnu.append(100.0 * lfPower / (lfPower + hfPower))
    hfnu.append(100.0 * hfPower / (lfPower + hfPower))
    lfhf.append(lfPower / hfPower)
    
    results = dict()
    results["VLFabs"] = np.median(vlfabs)
    results["LFabs"] = np.median(lfabs)
    results["HFabs"] = np.median(hfabs)
    results["LFnu"] = np.median(lfnu)
    results["HFnu"] = np.median(hfnu)
    results["LFHF"] = np.median(lfhf)

    return results

def count_time_domain(RR, x=50, binWidth=7.8125):
    result = dict()
    diffSeg = RR[1::1] - RR[0:-1:1]
    result["mean"] = np.mean(RR)
    result["sdnn"] = np.std(RR)
    result["rmssd"] = np.sqrt(np.mean(diffSeg * diffSeg))
    if np.mean(RR) < 20: 
        xAux = x/1000
    else: 
        xAux = x
    result["pnnx"] = 100*np.sum(np.abs(diffSeg) > xAux)/len(diffSeg)
    if np.mean(RR) < 20: 
        binwidthAux = binWidth/1000
    else: 
        binwidthAux = binWidth
    hist, edges = np.histogram(RR, bins=np.arange(min(RR), max(RR)+binwidthAux, binwidthAux))
    result["triang"] = len(RR)/np.max(hist)
    result["tinn"] = calcTINN(hist, edges)

    return result


def calcTINN(hist, edges):

    maxBin, maxHist = np.argmax(hist), np.max(hist)

    Nrange = range(0, maxBin + 1, 1)
    Mrange = range(maxBin, len(hist), 1)
    bestError = np.Inf
    bestN = 0
    bestM = len(hist) - 1
    for n in Nrange:
        for m in Mrange:
            error = 0

            # The region where the triangular fit is zero
            # From the beggining up to N (increasing)
            for left in range(0, n, 1):
                error += hist[left] ** 2
            # From the end up to M (decreasing)
            for right in range(m + 1, len(hist), 1):
                error += hist[right] ** 2

            # The region where the triangular fit is nonzero
            # From N to max
            upLine = np.linspace(0, maxHist, maxBin - n + 1)  # Range = [n,maxBin]
            error += np.sum((upLine - hist[n:maxBin + 1]) ** 2)

            # From max to M
            downLine = np.linspace(maxHist, 0, m - maxBin + 1)  # Range = [maxBin,m]
            error += np.sum((downLine[1:] - hist[maxBin + 1:m + 1]) ** 2)  # Discard the first point (max) already compared in upLine

            if error < bestError:
                bestError = error
                bestN = n
                bestM = m

    return (edges[bestM] - edges[bestN])