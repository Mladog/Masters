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
            self.artifacts = {"Auto T1": [],
                            "Auto T2": [],
                            "Auto T3": [],
                            "Manual T1": [],
                            "Manual T2": [],
                            "Manual T3": []}
        else:
            self.RR = self.get_RR_intervals()
            self.RR_vect = self.get_RR_vect()
            # zainicjowanie słownika artefaktów
            self.artifacts = {"Auto T1": [],
                            "Auto T2": [],
                            "Auto T3": [],
                            "Manual T1": [],
                            "Manual T2": [],
                            "Manual T3": []}
        
    def get_RR_intervals(self):
        with open(self.path) as f:
            lines = f.readlines()
        # usunięcie headera
        lines = lines[3:]
        # usunięcie pustych wierszy
        lines_tmp = []
        [lines_tmp.append(x.replace("\n", "")) for x in lines]
        if "" in lines_tmp:
            lines_tmp.remove("")
        # konwersja do np.array z elementami typu int
        list_int = np.array([int(x) for x in lines_tmp])
        return list_int

    def get_RR_vect(self):
        """
        Funkcja odpowiedzialna za utworzenie wektora zer i jedynek,
        w którym "1" oznacza miejsce wystąpienia załamka R. 
        """
        self.duration = np.sum(self.RR) # czas wyrażony w milisekundach
        print(sum(self.RR))
        peak_vect = np.zeros(int(self.duration))
        np.put(peak_vect, self.RR, 1)
        return peak_vect