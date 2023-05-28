# %%
import pandas as pd
from datetime import datetime
import numpy as np

PROBES_PATH = "C:/Users/mlado/Desktop/names.xlsx"
DIR_PATH = "C:/Users/mlado/Desktop/Mgr_new_data/prepared_data"

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

data = pd.read_excel(PROBES_PATH, header=0)
probes = data["supine_standing"].to_list()
file_names = data["file"].to_list()
dir_path = DIR_PATH

# 5 mins in ms
defined_time = 5*60*1000
# %%
for f in short_file_names:
    print(f)
    RRs, header = get_RR_intervals(f"{dir_path}/{f}/{f}_full_examination.txt")
    RRs_sum = RRs.cumsum(0)
    significant_probe = int(data[data["file"] == f]["supine_standing"])
    RRs_sum = RRs_sum - RRs_sum[significant_probe]
    RR_supine = RRs[(RRs_sum > -defined_time) & (RRs_sum <= 0)]
    RR_standing = RRs[(RRs_sum > 0) & (RRs_sum <= defined_time + RRs_sum[significant_probe + 1])]

    with open(f"{dir_path}/{f}/{f}_supine.txt", "w") as txt_file:
        for el in header:
            txt_file.write(f"{el}")
        for el in RR_supine:
            txt_file.write(f"{el}" + "\n")

    with open(f"{dir_path}/{f}/{f}_standing.txt", "w") as txt_file:
        for el in header:
            txt_file.write(f"{el}")
        for el in RR_standing:
            txt_file.write(f"{el}" + "\n")

# %%
