"""
Moduł odpowiedzialny za obsługę klasy Examination 
"""

import neurokit2 as nk
import numpy as np
from scipy.signal import savgol_filter, find_peaks

class Respiration():
    """
    klasa Respiration zawierajaca wszystkie metody i atrybuty dotyczace analizy 
    sygnalu oddechowego pochodzacego z pneumonitora impedancyjnego
    """
    def __init__(self, RR_signal, window_size=71, amplitude_min=0.2, min_distance = 30):
        # wyznaczenie poczatkow faz oddechowych
        self.signal, self.expiration_onsets, self.inspiration_onsets = self.find_extrema(RR_signal, window_size=window_size, min_distance =min_distance, amplitude_min=amplitude_min)
        # wyznaczenie czestotliwosci chwilowej
        self.fs_inst, self.breath_dur = self.get_fs_inst(RR_signal)
        # wyznaczenie dlugosci faz oddechowych
        self.dur_insp, self.dur_exp = self.get_dur(RR_signal)
        # wyznaczenie parametrow
        self.RRV_params = self.get_params()


    def get_fs_inst(self, RR_signal):
        """
        funkcja sluzaca obliczeniu czestotliwosci chwilowej sygnalu (RR - Respiratory Rate)
        """
        RR_cumsum = np.cumsum(RR_signal)
        #print(RR_cumsum)
        # wyznaczenie roznic czasowych miedzy kolejnymi poczatkami wdechow
        t_diff = [(j-i)/1000 for i, j in zip(RR_cumsum[self.inspiration_onsets[:-1]], RR_cumsum[self.inspiration_onsets[1:]])]
        # wyznaczenie częstości oddechowej
        return [60/t for t in t_diff], t_diff

    def get_dur(self, RR_signal):
        """
        funkcja sluzaca wyznaczeniu dlugosci faz wdechu oraz wydechu
        """
        RR_cumsum = np.cumsum(RR_signal)
        dur_insp = [(exp-insp)/1000 for insp, exp in zip(RR_cumsum[self.inspiration_onsets], RR_cumsum[self.expiration_onsets])]
        dur_exp = [(insp-exp)/1000 for insp, exp in zip(RR_cumsum[self.inspiration_onsets[1:]], RR_cumsum[self.expiration_onsets[:-1]])]
        return dur_insp, dur_exp

    def _rsp_findpeaks_outliers(self, rsp_cleaned, extrema, amplitude_min):
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

    def _rsp_findpeaks_sanitize(self, extrema, amplitudes):
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

    def _correct_extrema(self, signal, peaks, troughs):
        """
        korekcja wyszukanych miejsc wystąpienia maksimów i minimów
        poprawia efekt nadmiernego wygładzenia sygnału
        """
        peaks_tmp = []
        for peak in peaks:
            if 5 < peak < len(signal) - 5:
                vals = list(signal[peak-5:peak+6])
                max_index = vals.index(max(vals))
                max_index -= 5
                if max_index != 0:
                    peaks_tmp.append(peak + max_index)
                else:
                    peaks_tmp.append(peak)
            else:
                peaks_tmp.append(peak)
        
        troughs_tmp = []
        for trough in troughs:
            if 5 < trough < len(signal) - 5:
                vals = list(signal[trough-5:trough+6])
                min_index = vals.index(min(vals))
                min_index -= 5
                if min_index != 0:
                    troughs_tmp.append(trough + min_index)
                else:
                    troughs_tmp.append(trough)
            else:
                troughs_tmp.append(trough)
        
        return peaks_tmp, troughs_tmp
        

    def find_extrema(self, signal, window_size = 71, poly_order = 5, min_distance = 30, amplitude_min=0.2):
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
        extrema, amplitudes = self._rsp_findpeaks_outliers(smoothed_signal, extrema, amplitude_min)
        
        # wydobycie ostatecznego zbioru wartości
        peaks, troughs = self._rsp_findpeaks_sanitize(extrema, amplitudes)
        peaks, troughs = self._correct_extrema(signal, peaks, troughs)

        return smoothed_signal, peaks, troughs

    def get_params(self):
        diffSeg = np.array(self.breath_dur[1::1]) - np.array(self.breath_dur[0:-1:1])
        RRV_params = dict()
        RRV_params["mean"] = np.mean(self.breath_dur)
        RRV_params["std"] = np.std(self.breath_dur)
        RRV_params["rmssd"] = np.sqrt(np.mean(diffSeg * diffSeg))
        RRV_params["exp/inp_rate"] = np.mean(self.dur_exp)/np.mean(self.dur_insp)
        RRV_params["mean_fs_inst"] = np.mean(self.fs_inst)
        return RRV_params