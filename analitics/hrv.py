import numpy as np
from statsmodels.tsa.stattools import adfuller
import scipy

def count_hrv(RR):
    stationarity_result = adfuller(RR)[1]
    hrv_params = {"stationarity": stationarity_result,
                "hrv_time": count_time_domain(RR),
                "hrv_nonlinear": count_nonlinear(RR)
            }

    if stationarity_result:
        hrv_params["hrv_freq"] = count_freq_domain(RR)
    
    return hrv_params


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
    results["VLF"] = np.sum(psd[vlfRange]) * freqResol
    results["LF"] = np.sum(psd[lfRange]) * freqResol
    results["HF"] = np.sum(psd[hfRange]) * freqResol
    results["LFnu"] = 100.0 * results["LF"] / (results["LF"] + results["HF"])
    results["HFnu"] = 100.0 * results["HF"] / (results["LF"] + results["HF"])
    results["LFHF"] = results["LF"] / results["HF"]

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