# %%
import numpy as np
# %%
path = "C:/Users/mlado/Desktop/Masters/Dane/21102002_Bienias Dominik.txt"
with open(path) as f:
    lines = f.readlines()
# usunięcie headera
header = lines[:3]
new_lines = lines[3:]
# usunięcie pustych wierszy
lines_tmp = []
[lines_tmp.append(x.replace("\n", "")) for x in new_lines]
if "" in lines_tmp:
    lines_tmp.remove("")
# konwersja do np.array z elementami typu int
list_int = np.array([int(x.split("\t")[-1]) for x in lines_tmp])

# %%

path = "C:/Users/mlado/Desktop/Masters/Dane/21102002_Bienias Dominik.txt"
with open(path) as f:
    lines = f.readlines()

vals = [s for s in lines if s.strip().isdigit()]
lines_tmp = []
[lines_tmp.append(x.replace("\n", "")) for x in vals]
if "" in lines_tmp:
    lines_tmp.remove("")
list_int2 = np.array([int(x.split("\t")[-1]) for x in lines_tmp])
# %%
unique_elements = list(set(list_int) - set(list_int2))
# %%
