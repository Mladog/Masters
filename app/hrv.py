"""
Module responsible for signal analisys
"""

import numpy as np
#from hrvanalysis import get_time_domain_features, get_poincare_plot_features, get_frequency_domain_features, get_sampen
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
                  "hrv_nonlinear": count_nonlinear(obj.examination.RR[obj.exam_start:obj.exam_stop]),
                  "hrv_freq": count_freq_domain(obj.examination.RR[obj.exam_start:obj.exam_stop])
                }
    return hrv_params

def create_hrv_summary(hrv_params):
    if hrv_params["stationarity"] <= 0.05:
        stationarity_text = f"sygnał stacjonarny (p-wartość {round(hrv_params['stationarity'], 3)} dla testu adfuller)"
    else:
        stationarity_text = f"Uwaga, badanie niestacjonarne \n(p-wartość test adfuller: {round(hrv_params['stationarity'], 3)})\n"
    #stationarity_text = ""
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
    """
    funkcja odpowiedzialna za policzenie parametrow HRV
    w dziedzinie czestotliwosci
    """
    vlfBand = [0.0033, 0.04]
    lfBand = [0.04, 0.15]
    hfBand = [0.15, 0.4]
    interpRate = 3
    # stworzenie wektora czasu poprzez kumulacje czasow trwania
    # kolejnych interwalow RR
    timeSig_tmp = np.cumsum(RR).tolist()
    seriesSig = RR

    # zmiana czasu na sekundy, jesli podano ciag interwalow w ms
    medDiff = np.median([x - y for x, y in zip(timeSig_tmp[1:], timeSig_tmp[:-1])])
    if medDiff > 20:  
        timeSig_tmp = [t/1000 for t in timeSig_tmp]  # zmiana do sekund

    # wyznaczenie miejsc wystapienia interwalu jako wartosc srodkowa czasu jego wystapienia 
    timeSig = [timeSig_tmp[i-1]+ timeSig_tmp[i]/2 for i in range(1, len(timeSig_tmp))]
    timeSig.insert(0, timeSig[0]/2)

    # interpolacja
    funcInterp = scipy.interpolate.interp1d(timeSig, seriesSig, 'cubic')
    newTime = np.arange(timeSig[0], timeSig[-1], 1 / interpRate)
    newSeries = funcInterp(newTime)

    # wyznaczenie periodogramu
    f, psd = scipy.signal.periodogram(newSeries, interpRate, detrend='linear')
    vlfRange = (vlfBand[0] <= f) * (f <= vlfBand[1])
    lfRange = (lfBand[0] <= f) * (f <= lfBand[1])
    hfRange = (hfBand[0] <= f) * (f <= hfBand[1])

    freqResol = f[1]-f[0]
    results = dict()
    results["VLFabs"] = np.sum(psd[vlfRange]) * freqResol
    results["LFabs"] = np.sum(psd[lfRange]) * freqResol
    results["HFabs"] = np.sum(psd[hfRange]) * freqResol
    results["LFnu"] = 100.0 * results["LFabs"] / (results["LFabs"] + results["HFabs"])
    results["HFnu"] = 100.0 * results["HFabs"] / (results["LFabs"] + results["HFabs"])
    results["LFHF"] = results["LFabs"] / results["HFabs"]

    return results

def count_nonlinear(RR):
    diff_rr_intervals = np.diff(RR)
    results = dict()
    # szerokosc elipsy Pointcare
    results["sd1"] = np.sqrt(np.std(diff_rr_intervals, ddof=1) ** 2 * 0.5)
    # dlugosc elipsy Pointcare
    results["sd2"] = np.sqrt(2 * np.std(RR, ddof=1) ** 2 - 0.5 * np.std(diff_rr_intervals, ddof=1) ** 2)
    return results

def count_time_domain(RR, x=50, binWidth=7.8125):
    """
    parametry liczone w dziedzinie czestotliwosci
    """
    result = dict()
    diffSeg = RR[1::1] - RR[0:-1:1]
    result["mean"] = np.mean(RR)
    result["sdnn"] = np.std(RR)
    result["rmssd"] = np.sqrt(np.mean(diffSeg * diffSeg))
    # zmiana czasu na sekundy, jesli podano ciag interwalow w ms
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