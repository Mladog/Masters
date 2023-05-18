# %%
import numpy as np
from scipy import interpolate
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt

def get_RR_intervals(path):
    with open(path) as f:
        lines = f.readlines()
    lines = lines[3:]
    # usunięcie pustych wierszy
    lines_tmp = []
    [lines_tmp.append(x.replace("\n", "")) for x in lines]
    if "" in lines_tmp:
        lines_tmp.remove("")
    # konwersja do np.array z elementami typu int
    list_int = np.array([int(x.split("\t")[-1]) for x in lines_tmp])
    return list_int

def find_art1(diff, RR):
    """
    funkcja do wyszukiwania artefaktów typu 1
    """
    # obliczone różnice między obecnym i poprzednim interwałem
    d_prev = [1 if abs(d) > diff else 0 for d in RR[1:] - RR[:-1]]
    d_prev.insert(0, 0)
    # obliczone różnice między obecnym i następnym interwałem
    d_next = [1 if abs(d) > diff else 0 for d in RR[:-1] - RR[1:]]
    d_next.insert(-1, 0)

    # wyszukanie miejsc, w których próbka ma diff ms rożnicy między zarówno
    # poprzednim jak i następnym interwałem
    final_list = [sum(value) for value in zip(d_prev, d_next)]
    idx = np.where(np.array(final_list) == 2)[0]

    return idx.tolist()

def find_art2(diff, RR, diff_1=200):
    """
    funkcja do wyszukiwania artefaktów typu 2 - długi interwał po którym następuje krótki interwał
    """
    # obliczone różnice między obecnym i następnym interwałem
    d_next = [1 if d > diff else 0 for d in RR[:-1] - RR[1:]]
    d_next.insert(-1, 0)

    # wyszukanie miejsc, w których próbka ma diff ms rożnicy między zarówno
    # poprzednim jak i następnym interwałem
    idx = np.where(np.array(d_next) == 1)[0]
    art1 = find_art1(diff_1, RR)
    
    final = [x for x in idx if min(art1 - x) >1]
    return final

def find_art3(diff, RR, diff_1=200):
    """
    funkcja do wyszukiwania artefaktów typu 3 - krótki interwał po którym następuje długi interwał
    """
    # obliczone różnice między obecnym i następnym interwałem
    d_next = [1 if -d > diff else 0 for d in RR[:-1] - RR[1:]]
    d_next.insert(-1, 0)

    # wyszukanie miejsc, w których próbka ma diff ms rożnicy między zarówno
    # poprzednim jak i następnym interwałem
    idx = np.where(np.array(d_next) == 1)[0]
    art1 = find_art1(diff_1, RR)
    final = [x for x in idx if min(art1 - x) > 1]
    return final

def remove_artifacts(RR, artifacts_list, method = "interpolacja liniowa"):
    if len(artifacts_list) > 0:
        RR_copy = [float(R) for R in RR]
        for i in artifacts_list:
            RR_copy[int(i)] = np.nan

        RR_with_nan = np.array(RR_copy)
        inds = np.arange(RR_with_nan.shape[0])
        values = np.where(np.isfinite(RR_with_nan))
        nan_values = np.where(~np.isfinite(RR_with_nan))

        deleted = np.empty(0)
        if method == "interpolacja liniowa":
            f = interpolate.interp1d(inds[values], RR_with_nan[values], bounds_error=False)
            RR_interpolated = np.where(np.isfinite(RR_with_nan), RR_with_nan, f(inds))
        elif method == "usunięcie":
            RR_interpolated = np.delete(RR_with_nan, np.where(~np.isfinite(RR_with_nan)))
            deleted = np.where(~np.isfinite(RR_with_nan))
        return RR_interpolated
    else:
        return RR

artifacts = {"T1": 0,
            "T2": 0,
            "T3": 0,
            "different": 0}

path = "C:/Users/mlado/Desktop/Mgr_new_data/raw_data/Ziewiecki_Rafał_2.txt"
RR = get_RR_intervals(path)
a1 = [0]; a2 =[0]; a3=[0]

a1_prev = find_art1(200, RR)
print(f"a1: {len(a1)}")
a2_prev = find_art2(400, RR, 200)
print(f"a2: {len(a2)}")
a3_prev = find_art3(400, RR, 200)



# %%
