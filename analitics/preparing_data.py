# %%


"""from examination import Examination
ex = Examination(searchig_value=18)

plt.plot(ex.RR_yoyo)"""
import pandas as pd
from datetime import datetime
import numpy as np

def get_RR_intervals(path):
    with open(path) as f:
        lines = f.readlines()
    # usunięcie headera
    header = lines[:3]
    lines = lines[3:]
    # usunięcie pustych wierszy
    lines_tmp = []
    [lines_tmp.append(x.replace("\n", "")) for x in lines]
    if "" in lines_tmp:
        lines_tmp.remove("")
    # konwersja do np.array z elementami typu int
    list_int = np.array([int(x.split("\t")[-1]) for x in lines_tmp])
    return list_int, header

data = pd.read_excel("C:/Users/mlado/Desktop/Mgr_new_data/Matryca_danych2.xlsx")

start_time = data['Rejestracja przed próbą - CZAS STARTU\nSTART']
t1 = data['Test ortostatyczny 5-5 min\nGodzina rozpoczęcia SUPINE']
t2 = data['Test ortostatyczny 5-5 min\nGodzina rozpoczęcia STANDING']
t3 = data['Rozgrzewka godzina rozpoczecia']
t4 = data['Yo-Yo Test godzina rozpoczęcia']
t5 = data['Godzian rozpoczecia recovery 5 min po Yo-Yo']
t6 = data['Godzian zakończenia recovery 5 min po Yo-Yo']
t7 = data['Yo-Yo czas [min., sek.]']

new_col_names = ["start", "supine", "standing", "warmup", "Yoyo", "recovery", "end"]
new_df = pd.DataFrame(columns=new_col_names)
for col_name, time in zip(new_col_names, [start_time, t1, t2, t3, t4, t5, t6]):
    new_df[col_name] = [(t.hour * 60 + t.minute) * 60 + t.second for t in time]

new_df = new_df.sub(new_df['start'], axis=0)

new_df["Yoyo_duration"] = [(t.hour * 60 + t.minute) * 60 + t.second for t in t7]


new_names = []
for name in data["Nazwisko"].to_list():
    if " " in name:
        new_names.append(name[:-1])
    else:
        new_names.append(name)

new_df["surname"] = new_names
new_df["name"] = data["Imię"]

t1 = []; t11 = []; t2 = []; t22 = []; t3 =[]; t4=[]; t44=[]; t5=[]; t6=[]
new_df["path"] = data["Ścieżka"]

"""new_paths = []
for path in data["Ścieżka"].to_list():
    new_paths.append(path.replace("\\data\\", "\\raw_data\\"))"""


for index, row in new_df.iterrows():
    RR_df = pd.DataFrame()
    RR_intervals, _ = get_RR_intervals(row["path"])
    RR_df["intervals"] = RR_intervals
    RR_df.reset_index()
    cumsum = RR_df["intervals"].cumsum()
    t1.append(sum(cumsum < row["supine"]*1000))
    t11.append(sum(cumsum < (row["supine"]+5*60)*1000))
    t2.append(sum(cumsum < row["standing"]*1000))
    t22.append(sum(cumsum < (row["standing"]+5*60)*1000))
    t3.append(sum(cumsum < row["warmup"]*1000))
    t4.append(sum(cumsum < row["Yoyo"]*1000))
    t44.append(sum(cumsum < (row["Yoyo"]+row["Yoyo_duration"])*1000))
    t5.append(sum(cumsum < row["recovery"]*1000))
    t6.append(sum(cumsum < row["end"]*1000))

new_df["supine_start_probe"] = t1
new_df["supine_end_probe"] = t11
new_df["standing_start_probe"] = t2
new_df["standing_end_probe"] = t22
new_df["warmup_start_probe"] = t3
new_df["Yoyo_start_probe"] = t4
new_df["Yoyo_end_probe"] = t44
new_df["recovery_start_probe"] = t5
new_df["end_probe"] = t6

#new_df.to_excel("C:/Users/mlado/Desktop/probes.xlsx")
list_of_files = []
for index, row in new_df.iterrows():
    list_of_files.append(f"{index+1}_{row['surname']}")

pd.DataFrame(list_of_files).to_excel("C:/Users/mlado/Desktop/names.xlsx")
# %%

for index, row in new_df.iterrows():
    os.mkdir(f"C:/Users/mlado/Desktop/Mgr_new_data/prepared_data/{index+1}_{row['surname']}")
    RR_intervals, header = get_RR_intervals(row["path"])
    new_path = f"C:/Users/mlado/Desktop/Mgr_new_data/prepared_data/{index+1}_{row['surname']}/{index+1}_{row['surname']}"
    with open(f"{new_path}_full_examination.txt", "w") as txt_file:
        for el in header:
            txt_file.write(f"{el}")
        for el in RR_intervals:
            txt_file.write(f"{el}" + "\n")
    
    """with open(f"{new_path}_full.txt", "w") as txt_file:
        for el in header:
            txt_file.write(f"{el}")
        for el in RR_intervals[row["supine_start_probe"]:row["end_probe"]]:
            txt_file.write(f"{el}" + "\n")

    with open(f"{new_path}_supine.txt", "w") as txt_file:
        for el in header:
            txt_file.write(f"{el}")
        for el in RR_intervals[row["supine_start_probe"]:row["supine_end_probe"]]:
            txt_file.write(f"{el}" + "\n")

    with open(f"{new_path}_standing.txt", "w") as txt_file:
        for el in header:
            txt_file.write(f"{el}")
        for el in RR_intervals[row["standing_start_probe"]:row["standing_end_probe"]]:
            txt_file.write(f"{el}" + "\n")

    with open(f"{new_path}_warmup.txt", "w") as txt_file:
        for el in header:
            txt_file.write(f"{el}")
        for el in RR_intervals[row["warmup_start_probe"]:row["Yoyo_start_probe"]]:
            txt_file.write(f"{el}" + "\n")

    with open(f"{new_path}_yoyo.txt", "w") as txt_file:
        for el in header:
            txt_file.write(f"{el}")
        for el in RR_intervals[row["Yoyo_start_probe"]:row["Yoyo_end_probe"]]:
            txt_file.write(f"{el}" + "\n")

    with open(f"{new_path}_recovery.txt", "w") as txt_file:
        for el in header:
            txt_file.write(f"{el}")
        for el in RR_intervals[row["recovery_start_probe"]:row["end_probe"]]:
            txt_file.write(f"{el}" + "\n")"""


# %%
