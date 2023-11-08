"""
Examination Class
"""
import numpy as np
from interval import Interval


class Examination():
    def __init__(self, path=None):
        self.path = path
        if self.path == None:
            self.RR = []
            self.t = []
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
            self.deleted_artifacts = 0

        else:
            self.RR = self.get_RR_intervals()
            self.RR_intervals = [Interval(RR) for RR in self.RR]
            # zainicjowanie słownika artefaktów
            self.artifacts = {"T1_auto": [],
                            "T2_auto": [],
                            "T3_auto": [],
                            "T1_manual": [],
                            "T2_manual": [],
                            "T3_manual": [],
                            "other_manual": []}

            self.corrected_artifacts = {"T1_auto": 0,
                            "T2_auto": 0,
                            "T3_auto": 0,
                            "T1_manual": 0,
                            "T2_manual": 0,
                            "T3_manual": 0,
                            "other_manual": 0}
            self.deleted_artifacts = 0
        
    def get_RR_intervals(self):
        with open(self.path) as f:
            lines = f.readlines()

        vals = [s for s in lines if s.strip().isdigit()]
        lines_tmp = []
        [lines_tmp.append(x.replace("\n", "")) for x in vals]
        if "" in lines_tmp:
            lines_tmp.remove("")
        list_int = np.array([int(x.split("\t")[-1]) for x in lines_tmp])
        return list_int

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