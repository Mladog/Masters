# %%
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

data = pd.read_excel("C:/Users/mlado/Desktop/nowa_matryca.xlsx")
data_new = data[110:]
data_new.reset_index(inplace = True)

print(len(data_new["Nazwisko"]))
print(len(data_new["Nazwisko"].unique()))
# %%

data_new["Nazwisko"] = data_new["Nazwisko"].str.replace(" ", "")

"""new_df["surname"] = new_names
new_df["name"] = data["Imię"]

t1 = []; t11 = []; t2 = []; t22 = []; t3 =[]; t4=[]; t44=[]; t5=[]; t6=[]
new_df["path"] = data["Ścieżka"]
"""
"""new_paths = []
for path in data["Ścieżka"].to_list():
    new_paths.append(path.replace("\\data\\", "\\raw_data\\"))"""


#new_df.to_excel("C:/Users/mlado/Desktop/probes.xlsx")
list_of_files = []
for index, row in data_new.iterrows():
    list_of_files.append(f"{index+1}_{row['Nazwisko']}")

#pd.DataFrame(list_of_files).to_excel("C:/Users/mlado/Desktop/names.xlsx")
# %%
res = os.listdir("C:/Users/mlado/Desktop/Mgr_new_data/prepared_data")

for index, row in data_new.iterrows():
    matching = [s for s in res if row['Nazwisko'] in s]
    if len(matching) == 1:
        os.mkdir(f"C:/Users/mlado/Desktop/Mgr_new_data/prepared_data/{index+111}_{row['Nazwisko']}")
        RR_intervals, header = get_RR_intervals(f"C:/Users/mlado/Desktop/new_RR/{matching[0]}")
        new_path = f"C:/Users/mlado/Desktop/Mgr_new_data/prepared_data/{index+111}_{row['Nazwisko']}/{index+111}_{row['Nazwisko']}"
        with open(f"{new_path}_full_examination.txt", "w") as txt_file:
            for el in header:
                txt_file.write(f"{el}")
            for el in RR_intervals:
                txt_file.write(f"{el}" + "\n")
    else:
        print(index)
    
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
