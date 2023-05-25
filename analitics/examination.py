# %%
from constants import *
from respiration import Respiration
import numpy as np
import matplotlib.pyplot as plt
from hrv import count_hrv

DURATION_RANGE_STATIC = (60/30, 60/10)
DURATION_RANGE_YOYO = (60/60, 60/15)

class Examination():
    """
    Klasa Examination zawierająca informacje o sygnale
    """
    def __init__(self, folder_name, clean = True):
        self. folder_name = folder_name
        if clean:
            self.RR_yoyo = self._get_RRs(yoyo_clean_ext)
            self.RR_supine = self._get_RRs(supine_clean_ext)
            self.RR_standing = self._get_RRs(standing_clean_ext)

            self.respiration_yoyo = Respiration(self.RR_yoyo, DURATION_RANGE_YOYO)
            self.respiration_supine = Respiration(self.RR_supine, DURATION_RANGE_STATIC)
            self.respiration_standing = Respiration(self.RR_standing, DURATION_RANGE_STATIC)
        else:
            self.RR_yoyo = self._get_RRs(yoyo_ext)
            self.RR_supine = self._get_RRs(supine_ext)
            self.RR_standing = self._get_RRs(standing_ext)
            self.respiration_yoyo = None
            self.respiration_supine = None
            self.respiration_standing = None
        
        self.HRV_yoyo = self.get_hrv(self.RR_yoyo)
        self.HRV_supine = self.get_hrv(self.RR_supine)
        self.HRV_standing = self.get_hrv(self.RR_standing)


    def _get_RRs(self, extension):
        with open(f"{ROOT_DIR}/{self.folder_name}/{self.folder_name}{extension}") as f:
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
    
    def get_hrv(self, RR):
        res = count_hrv(RR)
        return res

#ex = Examination("72_Gaca")

"""plt.plot(ex.RR_yoyo)
plt.scatter(ex.respiration_yoyo.inspiration_onsets, ex.RR_yoyo[ex.respiration_yoyo.inspiration_onsets],
        color='r')
plt.scatter(ex.respiration_yoyo.expiration_onsets, ex.RR_yoyo[ex.respiration_yoyo.expiration_onsets],
        color='g')"""

"""plt.plot(ex.RR_supine)
plt.title('Wykryte początki wdechów i wydechów na sygnale RR')
plt.scatter(ex.respiration_supine.inspiration_onsets, ex.RR_supine[ex.respiration_supine.inspiration_onsets],
        color='r')
plt.scatter(ex.respiration_supine.expiration_onsets, ex.RR_supine[ex.respiration_supine.expiration_onsets],
        color='g')
plt.legend(['Surowy sygnał interwałów RR', 'Maksima - początki faz wydechu', 'Minima - początki faz wdechu'])
plt.xlabel('Długość interwału RR [ms]')
plt.ylabel('Numer interwału RR')"""

"""plt.plot(ex.respiration_standing.signal)
plt.scatter(ex.respiration_standing.inspiration_onsets, ex.respiration_standing.signal[ex.respiration_standing.inspiration_onsets],
        color='r')
plt.scatter(ex.respiration_standing.expiration_onsets, ex.respiration_standing.signal[ex.respiration_standing.expiration_onsets],
        color='g')"""

# %%
