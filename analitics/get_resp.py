# %%
import neurokit2 as nk
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

def get_RR_intervals(path):
    with open(path) as f:
        lines = f.readlines()
    # usunięcie headera
    lines = lines[3:]
    # usunięcie pustych wierszy
    lines_tmp = []
    [lines_tmp.append(x.replace("\n", "")) for x in lines]
    if "" in lines_tmp:
        lines_tmp.remove("")
    # konwersja do np.array z elementami typu int
    list_int = np.array([int(x.split("\t")[-1]) for x in lines_tmp])
    return list_int

# %%
path = "C:/Users/mlado/Desktop/Mgr_new_data/prepared_data/71_Skrok/71_Skrok_yoyo_clean.txt"
RR = get_RR_intervals(path)

def rsp_findpeaks_outliers(rsp_cleaned, extrema, amplitude_min=0.2):
    """
    Funkcja odpowiedzialna za usunięcie ze zbiory wykrytych ekstremów wskazań fałszywych
    """

    # Usunięcie ekstrem, które nie spełniają warunku minimalnej odległości 
    # od sąsiedniego ekstrema. Wartość jest ustalana indywidualnie dla 
    # każdego badania na podstawie mediany odleglosci miedzy wykrytymi ekstremami

    vertical_diff = np.abs(np.diff(rsp_cleaned[extrema]))
    median_diff = np.median(vertical_diff)
    min_diff = np.where(vertical_diff > (median_diff * amplitude_min))[0]
    extrema = extrema[min_diff]

    # Upewnienie się, że po każdym maksimum, istnieje minimum. W przeciwnym
    # przypadku - usunięcie nadmiarowego ekstrema.
    amplitudes = rsp_cleaned[extrema]
    extdiffs = np.sign(np.diff(amplitudes))
    extdiffs = np.add(extdiffs[0:-1], extdiffs[1:])
    removeext = np.where(extdiffs != 0)[0] + 1
    extrema = np.delete(extrema, removeext)
    amplitudes = np.delete(amplitudes, removeext)

    return extrema, amplitudes

def rsp_findpeaks_sanitize(extrema, amplitudes):
    """
    funckja odpowiedzialna za ujednolicenie zbioru
    zbior dostosowywany jest w ten sposób, aby zaczynał się od 
    minimum, a kończy na maksimum
    """
    if amplitudes[0] > amplitudes[1]:
        extrema = np.delete(extrema, 0)
    if amplitudes[-1] < amplitudes[-2]:
        extrema = np.delete(extrema, -1)
    peaks = extrema[1::2]
    troughs = extrema[0:-1:2]

    return peaks, troughs

def find_extrema(signal, window_size, poly_order, min_distance):
    """
    funkcja odpowiedzialna za wyszukanie ekstremow
    """
    # filtracja Savicky-Golay
    smoothed_signal = savgol_filter(signal, window_size, poly_order)

    # Znalezienie maksimów przy pomocy biblioteki scipy
    peaks, _ = find_peaks(smoothed_signal, distance=min_distance)

    # Znalezienie minimów przy pomocy biblioteki scipy
    negative_signal = -signal
    troughs, _ = find_peaks(negative_signal, distance=min_distance)

    # połączenie powyższych zbiorów i posortowanie według kolejności występowania
    extrema = np.sort(np.concatenate((peaks, troughs)))

    # usunięcie fałszywych wskazań
    extrema, amplitudes = rsp_findpeaks_outliers(smoothed_signal, extrema, amplitude_min=0.3)
    
    # wydobycie ostatecznego zbioru wartości
    peaks, troughs = rsp_findpeaks_sanitize(extrema, amplitudes)

    return peaks, troughs, smoothed_signal


peaks, troughs, smoothed = find_extrema(RR, 71, 5, 30)

"""
plt.plot(RR)
plt.plot(smoothed, 'g--')
plt.title('Wykryte początki wdechów i wydechów na sygnale RR')
plt.scatter(peaks, RR[peaks], color="r")
plt.scatter(troughs, RR[troughs], color="orange")
plt.legend(['Surowy sygnał interwałów RR', 'Wygładzony wygnał interwałów RR', 'Maksima', 'Minima'])
"""



# %%
