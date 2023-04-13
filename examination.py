"""
Examination Class
"""
import numpy as np


class Examination():
    def __init__(self, path=None):
        self.path = path
        if self.path == None:
            self.RR = []
            self.RR_vect = []
            self.duration = 0
            # zainicjowanie słownika artefaktów
            self.artifacts = {"T1_auto": [],
                            "T2_auto": [],
                            "T3_auto": [],
                            "T1_manual": [],
                            "T2_manual": [],
                            "T3_manual": []}
        else:
            self.RR = np.genfromtxt(self.path, delimiter=",").astype(int)
            self.RR_vect = self.get_RR_vect()
            # zainicjowanie słownika artefaktów
            self.artifacts = {"T1_auto": [],
                              "T2_auto": [],
                              "T3_auto": [],
                              "T1_manual": [],
                              "T2_manual": [],
                              "T3_manual": []}
        
    
    def get_RR_vect(self):
        """
        Funkcja odpowiedzialna za utworzenie wektora zer i jedynek,
        w którym "1" oznacza miejsce wystąpienia załamka R. 
        """
        self.duration = np.sum(self.RR) # czas wyrażony w milisekundach
        peak_vect = np.zeros(int(self.duration))
        np.put(peak_vect, self.RR, 1)
        return peak_vect