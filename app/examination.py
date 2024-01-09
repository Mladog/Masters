"""
Examination Class
"""
import numpy as np
from interval import Interval
import re
import pandas as pd
import openpyxl

class Examination():
    def __init__(self, path=None):
        self.path = path
        if self.path == None:
            self.RR = []
            self.t = []
            self.duration = 0
            self.extension = ''
            self.original_len = 0

        else:
            self.extension = self.path.split('.')[-1]
            self.RR = self.get_RR_intervals()
            self.RR_intervals = [Interval(RR) for RR in self.RR]
            self.original_len = len(self.RR_intervals)
            # zainicjowanie słownika artefaktów
            self.artifacts = {"T1_auto": [],
                            "T2_auto": [],
                            "T3_auto": [],
                            "T1_manual": [],
                            "T2_manual": [],
                            "T3_manual": [],
                            "other_manual": []}
        
    def get_RR_intervals(self):
        if self.extension == 'txt':
            with open(self.path) as f:
                lines = f.readlines()

            vals = [s for s in lines if re.match(r'^\s*-?\d+(\.\d+)?\s*$', s.strip()) is not None]
            lines_tmp = []
            [lines_tmp.append(x.replace("\n", "")) for x in vals]
            if "" in lines_tmp:
                lines_tmp.remove("")
            list_int = np.array([float(x.split("\t")[-1]) for x in lines_tmp])

        elif self.extension == 'xls':
            df = pd.read_excel(self.path, sheet_name=None)

            # Check if there are any worksheets in the Excel file
            if not df:
                raise ValueError("No worksheets found in the Excel file.")

            # Assuming the data is in the last column of the first sheet, you can modify accordingly
            first_sheet_name = list(df.keys())[0]
            last_column_name = df[first_sheet_name].columns[-1]

            # Extract values from the last column of the first sheet
            list_int = np.array(df[first_sheet_name][last_column_name].dropna().astype(float).tolist())

        elif self.extension == 'csv':
            df = pd.read_csv(self.path)

            # Assuming the data is in the last column, you can modify accordingly
            last_column_name = df.columns[-1]

            # Extract values from the last column
            list_int = np.array(df[last_column_name].dropna().astype(float).tolist())


        return list_int

    def save_to_txt(self, path=None, range=None):
        if path == None:
            path = f"{self.path[:-4]}_noartifacts.{self.extension}"
        if range == None:
            with open(f"{path}", "w") as txt_file:
                for el in self.RR_intervals:
                    txt_file.write(f"{el.value}" + "\n")
        else:
            with open(f"{path}", "w") as txt_file:
                for el in self.RR_intervals[range[0]:range[1]]:
                    txt_file.write(f"{el.value}" + "\n")