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
            self.header = []
            # zainicjowanie słownika artefaktów
            self.artifacts = {"T1_auto": [],
                            "T2_auto": [],
                            "T3_auto": [],
                            "T1_manual": [],
                            "T2_manual": [],
                            "T3_manual": [],
                            "inne_manual": []}

            self.corrected_artifacts = {"T1_auto": 0,
                            "T2_auto": 0,
                            "T3_auto": 0,
                            "T1_manual": 0,
                            "T2_manual": 0,
                            "T3_manual": 0,
                            "inne_manual": 0}
        else:
            self.RR = self.get_RR_intervals()
            self.RR_vect = self.get_RR_vect()
            # zainicjowanie słownika artefaktów
            self.artifacts = {"T1_auto": [],
                            "T2_auto": [],
                            "T3_auto": [],
                            "T1_manual": [],
                            "T2_manual": [],
                            "T3_manual": [],
                            "inne_manual": []}

            self.corrected_artifacts = {"T1_auto": 0,
                            "T2_auto": 0,
                            "T3_auto": 0,
                            "T1_manual": 0,
                            "T2_manual": 0,
                            "T3_manual": 0,
                            "inne_manual": 0}
        
    def get_RR_intervals(self):
        with open(self.path) as f:
            lines = f.readlines()
        # usunięcie headera
        self.header = lines[:3]
        lines = lines[3:]
        # usunięcie pustych wierszy
        lines_tmp = []
        [lines_tmp.append(x.replace("\n", "")) for x in lines]
        if "" in lines_tmp:
            lines_tmp.remove("")
        # konwersja do np.array z elementami typu int
        list_int = np.array([int(x.split("\t")[-1]) for x in lines_tmp])
        return list_int

    def get_RR_vect(self):
        """
        Funkcja odpowiedzialna za utworzenie wektora zer i jedynek,
        w którym "1" oznacza miejsce wystąpienia załamka R. 
        """
        self.duration = np.sum(self.RR) # czas wyrażony w milisekundach
        peak_vect = np.zeros(int(self.duration))
        np.put(peak_vect, self.RR, 1)
        return peak_vect

    def save_to_txt(self, path=None, range=None):
        if path == None:
            path = f"{self.path[:-4]}_noartifacts.txt"
        if range == None:
            with open(f"{path}", "w") as txt_file:
                for el in self.header:
                    txt_file.write(f"{el}")
                for el in self.RR:
                    txt_file.write(f"{el}" + "\n")
        else:
            with open(f"{path}", "w") as txt_file:
                for el in self.header:
                    txt_file.write(f"{el}")
                for el in self.RR[range[0]:range[1]]:
                    txt_file.write(f"{el}" + "\n")