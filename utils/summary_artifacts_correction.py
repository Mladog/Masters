# %%
import pandas as pd
from exams_to_drop import ExamsToDrop
import sqlite3
from examination import Examination
import numpy as np
import re
from constants import DATA_PATH

path = DATA_PATH
data = pd.read_excel(path, header=0)
data["Nazwisko"] = data["Nazwisko"].str.replace(" ", "")
data_clean = data[["Wiek kalendarzowy ", "Yo-Yo level [ilość]", "Yo-Yo dystans [m]", "Yo-Yo VO2max [ml/kg/min]", "Yo-Yo training load"]]
data_clean["folder_name"] = [f"{index+1}_{row['Nazwisko']}" for index, row in data.iterrows()]
data_clean=data_clean[~data_clean["folder_name"].isin(ExamsToDrop)]

competitor =data_clean.iloc[1]["folder_name"] 
df = pd.DataFrame(columns=["competitor", "correction_auto", "correction_manual", "deleted"])

for competitor in data_clean["folder_name"]:
    print(competitor)
    ex = Examination(competitor)
    ex_original = Examination(competitor, False)

    txt = f"C:/Users/mlado/Desktop/Mgr_new_data/prepared_data/{competitor}/{competitor}_supine_clean_stats.txt"
    # Read the contents of the text file
    with open(txt, 'r') as file:
        content = file.read()

    # Zdefiniowanie regular expression
    pattern_auto = r'\bT\d+_auto,\s*(\d+)\b'
    pattern_manual = r'\b(?:T[1-3]|inne)_manual,\s*(\d+)\b'

    # znalezienie cyfr przy uzyciu regular expression
    matches_manual = re.findall(pattern_manual, content)
    matches_auto = re.findall(pattern_auto, content)

    # zsumowanie wszystkich artefaktow
    sum_auto = np.sum([int(match) for match in matches_auto])
    sum_manual = np.sum([int(match) for match in matches_manual])

    # obliczenie liczby usunietych artefaktow
    deleted = len(ex_original.RR_supine) - len(ex.RR_supine)
    dict_to_add = {"competitor": competitor, "correction_auto": sum_auto, "correction_manual": sum_manual, "deleted": deleted}
    df = pd.concat([df, pd.DataFrame([dict_to_add])], ignore_index=True)

df.to_excel("supine_correction.xlsx")

# %%
