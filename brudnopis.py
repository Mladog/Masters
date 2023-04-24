# %%
"""
Module responsible for signal analisys
"""

from examination import Examination
from hrv import count_hrv
import matplotlib.pyplot as plt
import numpy as np

from scipy import interpolate
import scipy as sp
def fill_nan(RR_with_nan, method = "lin"):
    '''
    interpolate to fill nan values
    '''
    inds = np.arange(RR_with_nan.shape[0])
    values = np.where(np.isfinite(RR_with_nan))

    deleted = np.empty(0)
    if method == "lin":
        f = interpolate.interp1d(inds[values], RR_with_nan[values], bounds_error=False)
        RR_interpolated = np.where(np.isfinite(RR_with_nan), RR_with_nan, f(inds))

    elif method == "cub":
        f = sp.interpolate.CubicSpline(inds[values], RR_with_nan[values])
        RR_interpolated = np.where(np.isfinite(RR_with_nan),RR_with_nan,f(inds))
    
    elif method == "del":
        RR_interpolated = np.delete(RR_with_nan, np.where(~np.isfinite(RR_with_nan)))
        deleted = np.where(~np.isfinite(RR_with_nan))

    return RR_interpolated, deleted


def find_art1(examination, diff=200):
    """
    funkcja do wyszukiwania artefaktów typu 1
    """
    # obliczone różnice między obecnym i poprzednim interwałem
    d_prev = [1 if abs(d) > diff else 0 for d in examination.RR[1:] - examination.RR[:-1]]
    d_prev.insert(0, 0)
    # obliczone różnice między obecnym i następnym interwałem
    d_next = [1 if abs(d) > diff else 0 for d in examination.RR[:-1] - examination.RR[1:]]
    d_next.insert(-1, 0)

    # wyszukanie miejsc, w których próbka ma diff ms rożnicy między zarówno
    # poprzednim jak i następnym interwałem
    final_list = [sum(value) for value in zip(d_prev, d_next)]
    idx = np.where(np.array(final_list) == 2)[0]

    return idx.tolist()

def find_art2(examination, diff=200):
    """
    funkcja do wyszukiwania artefaktów typu 2 - długi interwał po którym następuje krótki interwał
    """
    # obliczone różnice między obecnym i następnym interwałem
    d_next = [1 if d > diff else 0 for d in examination.RR[:-1] - examination.RR[1:]]
    d_next.insert(-1, 0)

    # wyszukanie miejsc, w których próbka ma diff ms rożnicy między zarówno
    # poprzednim jak i następnym interwałem
    idx = np.where(np.array(d_next) == 1)[0]
    art1 = find_art1(obj)
    final = [x for x in idx if x not in art1]
    return final

def find_art3(examination, diff=200):
    """
    funkcja do wyszukiwania artefaktów typu 3 - krótki interwał po którym następuje długi interwał
    """
    # obliczone różnice między obecnym i następnym interwałem
    d_next = [1 if -d > diff else 0 for d in examination.RR[:-1] - examination.RR[1:]]
    d_next.insert(-1, 0)

    # wyszukanie miejsc, w których próbka ma diff ms rożnicy między zarówno
    # poprzednim jak i następnym interwałem
    idx = np.where(np.array(d_next) == 1)[0]
    art1 = find_art1(obj)
    final = [x for x in idx if x not in art1]
    return final


ex = Examination('C:/Users/mlado/Desktop/Masters/data/RRy z Yo-Yo/21102002_Snopczyński Jakub.txt')
hrv = count_hrv(ex)


plt.plot(ex.RR)
plt.plot(find_art1(ex), ex.RR[find_art1(ex)], 'ro')

idx = find_art1(ex)
RR_copy = ex.RR.astype("float")
for i in idx:
    RR_copy[i] = np.nan

new_RR_lin, d_l = fill_nan(RR_copy, "lin")
ex.RR = np.array([int(x) for x in new_RR_lin])
ex.get_RR_intervals()
new_RR_cub, d_c = fill_nan(RR_copy, "cub")
new_RR_del, d = fill_nan(RR_copy, "del")

plt.plot(ex.RR)

ex.save_to_txt()



# %%
