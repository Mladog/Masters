# %%
import pandas as pd
from exams_to_drop import ExamsToDrop
import sqlite3
from new_examination import Examination

path = "C:/Users/mlado/Desktop//nowa_matryca.xlsx"
data = pd.read_excel(path, header=0)
data_clean = data[["Wiek kalendarzowy ", "Yo-Yo level [ilość]", "Yo-Yo dystans [m]", "Yo-Yo VO2max [ml/kg/min]", "Yo-Yo training load"]]
data_clean["folder_name"] = [f"{index+1}_{row['Nazwisko']}" for index, row in data.iterrows()]
data_clean=data_clean[~data_clean["folder_name"].isin(ExamsToDrop)]

competitor =data_clean.iloc[1]["folder_name"] 

ex = Examination(competitor)
hrv_yoyo = ex.get_hrv(ex.RR_yoyo)
hrv_standing = ex.get_hrv(ex.RR_standing)
hrv_supine = ex.get_hrv(ex.RR_supine)
rrv_yoyo = ex.respiration_yoyo.RRV_params
rrv_standing = ex.respiration_standing.RRV_params
rrv_supine = ex.respiration_supine.RRV_params
# %%
