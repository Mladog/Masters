# %%
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from examination import Examination
ex = Examination(searchig_value=18)

plt.plot(ex.RR_yoyo)
# %%
import pandas as pd
from datetime import datetime

data = pd.read_excel("C:/Users/mlado/Desktop/Mgr_new_data/Matryca_danych.xlsx")


start_time = "2:13:57"
end_time = "11:46:38"

start_time = data['Rejestracja przed próbą - CZAS STARTU\nSTART']
t1 = data['Test ortostatyczny 5-5 min\nGodzina rozpoczęcia SUPINE']
t2 = data['Test ortostatyczny 5-5 min\nGodzina rozpoczęcia STANDING']
t3 = data['Rozgrzewka godzina rozpoczecia']
t4 = data['Yo-Yo Test godzina rozpoczęcia']
t5 = data['Godzian rozpoczecia recovery 5 min po Yo-Yo']
t6 = data['Godzian zakończenia recovery 5 min po Yo-Yo']


i = 0
new_col_names = ["start", "supine", "standing", "warmup", "Yoyo", "recovery", "end"]
new_df = pd.DataFrame(columns=new_col_names)
for col_name, time in zip(new_col_names, [start_time, t1, t2, t3, t4, t5, t6]):
    new_df[col_name] = [(t.hour * 60 + t.minute) * 60 + t.second for t in time]

new_df = new_df.sub(new_df['start'], axis=0)

new_df["Nazwisko"] = data["Nazwisko"]

# %%
