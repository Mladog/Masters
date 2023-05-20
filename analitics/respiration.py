"""
Moduł odpowiedzialny za obsługę klasy Examination 
"""

import neurokit2 as nk
import numpy as np

class Respiration():
    """
    klasa Respiration zawierajaca wszystkie metody i atrybuty dotyczace analizy 
    sygnalu oddechowego pochodzacego z pneumonitora impedancyjnego
    """
    def __init__(self, RR_signal):
        # wyznaczenie poczatkow faz oddechowych
        self.expiration_onsets, self.inspiration_onsets = self.find_extrema(RR_signal)
        # wyznaczenie czestotliwosci chwilowej
        self.get_fs_inst()
        # wyznaczenie objetosci oddechowej
        self.get_tv()
        # wyznaczenie dlugosci faz oddechowych
        self.get_dur()

    def get_fs_inst(self):
        """
        funkcja sluzaca obliczeniu czestotliwosci chwilowej sygnalu (RR - Respiratory Rate)
        """
        # wyznaczenie roznic czasowych miedzy kolejnymi poczatkami wdechow
        t_diff = [j/self.freq-i/self.freq for i, j in 
                    zip(self.inspiration_onsets[:-1], self.inspiration_onsets[1:])]
        # wyznaczenie częstości oddechowej
        self.fs_inst = [60/t for t in t_diff]

    def get_tv(self):
        """
        funkcja odpowiedzialna za wyznaczenie objetosci oddechowej
        """
        if self.expiration_onsets[0] > self.inspiration_onsets[0]:
            self.insp_depth = [max(self.signal_raw[this_exp:next_insp]) - min(self.signal_raw[prev_exp:this_insp]) 
                            for this_exp, next_insp, prev_exp, this_insp in 
                            zip(self.expiration_onsets[1:], self.inspiration_onsets[2:], self.expiration_onsets, self.inspiration_onsets[1:])]
            self.exp_depth = [-max(self.signal_raw[prev_insp:this_exp]) + min(self.signal_raw[this_insp:next_exp]) 
                            for prev_insp, this_exp, this_insp, next_exp in 
                            zip(self.inspiration_onsets, self.expiration_onsets, self.inspiration_onsets[1:], self.expiration_onsets[1:])]

        else:
            self.insp_depth = [max(self.signal[this_exp:next_insp]) - min(self.signal[prev_exp:this_insp]) 
                            for this_exp, next_insp, prev_exp, this_insp in 
                            zip(self.expiration_onsets[0:], self.inspiration_onsets[1:], self.expiration_onsets, self.inspiration_onsets[1:])]
            self.exp_depth = [-max(self.signal[prev_insp:this_exp]) + min(self.signal[this_insp:next_exp]) 
                            for prev_insp, this_exp, this_insp, next_exp in 
                            zip(self.inspiration_onsets, self.expiration_onsets[1:], self.inspiration_onsets[1:], self.expiration_onsets[2:])]

    def get_dur(self):
        """
        funkcja sluzaca wyznaczeniu dlugosci faz wdechu oraz wydechu
        """
        if self.expiration_onsets[0] > self.inspiration_onsets[0]:
            self.dur_insp = [insp/self.freq-exp/self.freq for insp, exp in zip(self.inspiration_onsets[1:], self.expiration_onsets)]
            self.dur_exp = [exp/self.freq-insp/self.freq for insp, exp in zip(self.inspiration_onsets, self.expiration_onsets)]
        else:
            self.dur_insp = [insp/self.freq-exp/self.freq for insp, exp in zip(self.inspiration_onsets[1:], self.expiration_onsets)]
            self.dur_exp = [exp/self.freq-insp/self.freq for insp, exp in zip(self.inspiration_onsets, self.expiration_onsets)]

    def trend(self):
        """
        funkcja sluzaca do wyznaczenia trendu w sygnale
        """
        print('trend not implemented')

    def complexity_note(self):
        """
        funkcja sluzaca do oceny zlozonosci sygnalu
        """
        print("complexity not implemented")

    def mov_average(self, window = 125):
        """
        funkcja sluzaca do wyznaczenia sredniej ruchomej sygnalu 
        """
        limit = len(self.signal) - int(len(self.signal)/window) - window
        moving_averages = [sum(self.signal[i:i+window])/window for i in range(limit)]

        return moving_averages
    
    def _rsp_findpeaks_outliers(self, extrema, amplitude_min=0.2):
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

    def _rsp_findpeaks_sanitize(extrema, amplitudes):
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

    def find_extrema(self, signal, window_size = 71, poly_order = 5, min_distance = 30):
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
        extrema, amplitudes = self._rsp_findpeaks_outliers(smoothed_signal, extrema, amplitude_min=0.3)
        
        # wydobycie ostatecznego zbioru wartości
        peaks, troughs = self._rsp_findpeaks_sanitize(extrema, amplitudes)

        return peaks, troughs
