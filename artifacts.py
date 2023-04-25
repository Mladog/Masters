"""
Moduł odpowiedziany za automatyczne wyznaczanie oraz usuwanie artefaktów
"""
import numpy as np
from scipy import interpolate
import scipy as sp
import pandas as pd

def find_art1(obj):
    """
    funkcja do wyszukiwania artefaktów typu 1
    """
    diff = int(obj.textbox_art1.text())
    # obliczone różnice między obecnym i poprzednim interwałem
    d_prev = [1 if abs(d) > diff else 0 for d in obj.examination.RR[1:] - obj.examination.RR[:-1]]
    d_prev.insert(0, 0)
    # obliczone różnice między obecnym i następnym interwałem
    d_next = [1 if abs(d) > diff else 0 for d in obj.examination.RR[:-1] - obj.examination.RR[1:]]
    d_next.insert(-1, 0)

    # wyszukanie miejsc, w których próbka ma diff ms rożnicy między zarówno
    # poprzednim jak i następnym interwałem
    final_list = [sum(value) for value in zip(d_prev, d_next)]
    idx = np.where(np.array(final_list) == 2)[0]

    return idx.tolist()

def find_art2(obj):
    """
    funkcja do wyszukiwania artefaktów typu 2 - długi interwał po którym następuje krótki interwał
    """
    diff = int(obj.textbox_art2.text())
    # obliczone różnice między obecnym i następnym interwałem
    d_next = [1 if d > diff else 0 for d in obj.examination.RR[:-1] - obj.examination.RR[1:]]
    d_next.insert(-1, 0)

    # wyszukanie miejsc, w których próbka ma diff ms rożnicy między zarówno
    # poprzednim jak i następnym interwałem
    idx = np.where(np.array(d_next) == 1)[0]
    art1 = find_art1(obj)
    final = [x for x in idx if x not in art1]
    return final

def find_art3(obj):
    """
    funkcja do wyszukiwania artefaktów typu 3 - krótki interwał po którym następuje długi interwał
    """
    diff = int(obj.textbox_art3.text())
    # obliczone różnice między obecnym i następnym interwałem
    d_next = [1 if -d > diff else 0 for d in obj.examination.RR[:-1] - obj.examination.RR[1:]]
    d_next.insert(-1, 0)

    # wyszukanie miejsc, w których próbka ma diff ms rożnicy między zarówno
    # poprzednim jak i następnym interwałem
    idx = np.where(np.array(d_next) == 1)[0]
    art1 = find_art1(obj)
    final = [x for x in idx if x not in art1]
    return final

def remove_artifacts(obj):
    '''
    funkcja zmieniająca wybrane artefakty
    '''
    atypes = obj.chosen_artifacts
    for m in [obj.m1, obj.m2, obj.m3]:
            if m.isChecked() == True:
                method = m.text()
    
    idx = np.array([])
    for atype in atypes:
        idx = np.append(idx, obj.examination.artifacts[atype])

    if len(idx) > 0:
        RR_copy = [float(R) for R in obj.examination.RR]
        for i in idx:
            RR_copy[int(i)] = np.nan

        RR_with_nan = np.array(RR_copy)
        inds = np.arange(RR_with_nan.shape[0])
        values = np.where(np.isfinite(RR_with_nan))
        nan_values = np.where(~np.isfinite(RR_with_nan))

        for val in inds[nan_values]:
            for key in obj.examination.artifacts.keys():
                if val in obj.examination.artifacts[key]:
                    obj.examination.artifacts[key].remove(val)

        deleted = np.empty(0)
        if method == "interpolacja liniowa":
            f = interpolate.interp1d(inds[values], RR_with_nan[values], bounds_error=False)
            RR_interpolated = np.where(np.isfinite(RR_with_nan), RR_with_nan, f(inds))

        elif method == "splajn kubiczny":
            f = sp.interpolate.CubicSpline(inds[values], RR_with_nan[values])
            RR_interpolated = np.where(np.isfinite(RR_with_nan),RR_with_nan,f(inds))
        
        elif method == "usunięcie":
            RR_interpolated = np.delete(RR_with_nan, np.where(~np.isfinite(RR_with_nan)))
            deleted = np.where(~np.isfinite(RR_with_nan))
            for val in inds[nan_values]:
                for key in obj.examination.artifacts.keys():
                    obj.examination.artifacts[key] = [x - 1 for x in obj.examination.artifacts[key] if x >=vals ]

        while np.isnan(RR_interpolated[0]):
            RR_interpolated = RR_interpolated[1:]
            # jesli usunieto 1. element - zaktualizować indeksy
            for key in obj.examination.artifacts.keys():
                obj.examination.artifacts[key] = [x - 1 for x in obj.examination.artifacts[key]]
        
        while np.isnan(RR_interpolated[-1]):
            RR_interpolated = RR_interpolated[:-1]
            for key in obj.examination.artifacts.keys():
                if len(RR_interpolated) in obj.examination.artifacts[key]:
                    obj.examination.artifacts[key].remove(len(RR_interpolated))

        obj.examination.RR = np.array([int(element) for element in RR_interpolated])
        #to_del = [el for el in deleted]
        return deleted
    else:
        return np.array([])

