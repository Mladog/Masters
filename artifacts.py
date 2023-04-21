"""
Moduł odpowiedziany za automatyczne wyznaczanie oraz usuwanie artefaktów
"""
import numpy as np
from scipy import interpolate
import scipy as sp

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
    method = obj.method

    idx = np.array(0)
    for atype in atypes:
        idx = np.append(idx, obj.examination.artifacts[atype])

    print(idx)
    #idx = np.unique(idx).astype(int)
    # podmienienie wartości wybranych typów artefkatów na np.nan
    values = np.empty(0); inds = np.empty(0); to_del = np.empty(0)
    if len(idx) > 0:
        RR_copy = obj.examination.RR.astype("float")
        for i in idx:
            RR_copy[i] = np.nan

        
        
        inds = np.arange(RR_copy.shape[0])
        values = np.where(np.isfinite(RR_copy))

        if method == "lin":
            f = interpolate.interp1d(inds[values], RR_copy[values], bounds_error=False)
            RR_temp = np.where(~np.isfinite(RR_copy), RR_copy, f(inds))
            print("RR_temp\n :")
            print(RR_temp)
            obj.examination.RR = np.array([int(x) for x in RR_temp])

        elif method == "cub":
            f = sp.interpolate.CubicSpline(inds[values], RR_copy[values])
            RR_temp = np.where(np.isfinite(RR_copy), RR_copy, f(inds))
            obj.examination.RR = np.array([int(x) for x in RR_temp])

        elif method == "del":
            RR_temp = np.delete(RR_copy, np.where(~np.isfinite(RR_copy)))
            to_del = np.where(~np.isfinite(RR_copy))
            obj.examination.RR = np.array([int(x) for x in RR_temp])

        print(obj.examination.RR)
    return to_del