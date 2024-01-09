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
    # count differences between this and previous interval
    d_prev = [1 if abs(obj.examination.RR_intervals[i].value - obj.examination.RR_intervals[i-1].value) > diff else 0 for i in range(1, len(obj.examination.RR_intervals))]
    d_prev.insert(0, 0)
    # count differences between this and next interval
    d_next = [1 if abs(obj.examination.RR_intervals[i-1].value - obj.examination.RR_intervals[i].value) > diff else 0 for i in range(1, len(obj.examination.RR_intervals))]
    d_next.insert(-1, 0)

    final_list = [sum(value) for value in zip(d_prev, d_next)]
    idx = np.where(np.array(final_list) == 2)[0]

    return idx.tolist()

def find_art2(obj):
    """
    funkcja do wyszukiwania artefaktów typu 2 - długi interwał po którym następuje krótki interwał
    """
    diff = int(obj.textbox_art2.text())
    # obliczone różnice między obecnym i następnym interwałem
    d_next = [1 if (obj.examination.RR_intervals[i-1].value - obj.examination.RR_intervals[i].value) > diff else 0 for i in range(1, len(obj.examination.RR_intervals))]
    d_next.insert(-1, 0)

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
    d_next = [1 if (obj.examination.RR_intervals[i-1].value - obj.examination.RR_intervals[i].value) > diff else 0 for i in range(1, len(obj.examination.RR_intervals))]
    d_next.insert(-1, 0)

    idx = np.where(np.array(d_next) == 1)[0]
    art1 = find_art1(obj)
    final = [x for x in idx if x not in art1]
    return final

def remove_artifacts(obj):
    '''
    function to change chosen artifacts
    '''
    # odczyt wybranych przez uzytkownika artefaktow wybranych do usuniecia
    atypes = obj.chosen_artifacts
    # sprawdzenie wybranej metody korekcji artefaktow
    for m in [obj.m1, obj.m2, obj.m3, obj.m4, obj.m5]:
        if m.isChecked() == True:
            method = m.text()
    
    idx = np.array([])
    for atype in atypes:
        # dodanie odczytanych artefaktow do listy przeznaczonej do skorygowania
        for el in obj.examination.artifacts[atype]:
            if (el >= obj.exam_start and el <= obj.exam_stop):
                idx = np.append(idx, el)
                if obj.examination.RR_intervals[int(el)].artifact == None:
                    obj.examination.RR_intervals[int(el)].artifact = atype

    # sprawdzenie ilosci
    if len(idx) > 0:
        for i in idx:
            obj.examination.RR_intervals[int(i)].value = np.nan

        RR_with_nan = np.array([interval.value for interval in obj.examination.RR_intervals])
        # utworzenie wektora indeksow
        inds = np.arange(RR_with_nan.shape[0])
        # odczytanie wartosci nieprzeznaczonych do usuniecia
        values = np.where(np.isfinite(RR_with_nan))
        # utworzenie wektora wartosci do usuniecia
        nan_values = np.where(~np.isfinite(RR_with_nan))

        deleted = np.empty(0)
        # korekcja metoda interpolacji liniowej
        if method == "linear interpolation":
            f = interpolate.interp1d(inds[~np.isnan(RR_with_nan)], RR_with_nan[~np.isnan(RR_with_nan)], bounds_error=False)

            for i, interval in enumerate(obj.examination.RR_intervals):
                # Check if the interval value needs correction (e.g., if it's NaN)
                if np.isnan(interval.value):
                    # Apply linear interpolation based on the index associated with the interval
                    interval.value = f(i)
                    interval.correction_methods[method] += 1

        # korekcja metoda splejnu kubicznego
        elif method == "cubic splain":
            f = sp.interpolate.CubicSpline(inds[values], RR_with_nan[values])
            for i, interval in enumerate(obj.examination.RR_intervals):
                # Check if the interval value needs correction (e.g., if it's NaN)
                if np.isnan(interval.value):
                    # Apply linear interpolation based on the index associated with the interval
                    interval.value = f(i)
                    interval.correction_methods[method] += 1
        
        # TO DO 
        # korekcja poprzez usuniecie 
        elif method == "deletion":
            obj.examination.deleted_artifacts += sum(np.isnan(interval.value) for interval in obj.examination.RR_intervals)
            obj.examination.RR_intervals = list(filter(lambda interval: not np.isnan(interval.value), obj.examination.RR_intervals))
                                                                                                                                                 

        # korekcja metoda sredniej kroczacej
        elif method == "moving average":
            for val in inds[nan_values]:
                # sprawdzenie warunku posiadania odpowiedniego sasiedztwa
                if 3 <= val <= len(obj.examination.RR_intervals) - 3:
                    neighborhood = RR_with_nan[val - 3:val + 4]
                    temp_means = []
                    for i in range(4):
                        temp_means.append(np.nanmean(neighborhood[i:i+4]))
                    
                    obj.examination.RR_intervals[val].value = np.mean(temp_means)
                    obj.examination.RR_intervals[val].correction_methods[method] += 1

                # jeśli przypadek skrajny o mniejszym sąsiedztwie niż zakładamy (+/-3) - interpolacja
                else:
                    f = interpolate.interp1d(inds[nan_values], RR_with_nan[nan_values], bounds_error=False)                            
                    if np.isnan(obj.examination.RR_intervals[val].value):
                        # Apply linear interpolation based on the index associated with the interval
                        obj.examination.RR_intervals[val].value = f(i)
                        obj.examination.RR_intervals[val].correction_methods["linear interpolation"] += 1

            # if any nans left (happen if there are many nans near each other or at the beggining/end - interpolate)
            RR_with_nan_new = np.array([interval.value for interval in obj.examination.RR_intervals])
            f = interpolate.interp1d(inds[~np.isnan(RR_with_nan_new)], RR_with_nan[~np.isnan(RR_with_nan_new)], bounds_error=False)
            for i, interval in enumerate(obj.examination.RR_intervals):
                # Check if the interval value needs correction (e.g., if it's NaN)
                if np.isnan(interval.value):
                    # Apply linear interpolation based on the index associated with the interval
                    interval.value = f(i)
                    interval.correction_methods["linear interpolation"] += 1

        elif method == "pre mean":
            for val in inds[nan_values]:
                value_from_gui = int(obj.pre_mean_count.currentText())
                # sprawdzenie warunku posiadania odpowiedniego sasiedztwa
                if value_from_gui <= val <= len(obj.examination.RR_intervals):
                    neighborhood = RR_with_nan[val - value_from_gui:val]
                    
                    obj.examination.RR_intervals[val].value = np.mean(neighborhood)
                    obj.examination.RR_intervals[val].correction_methods[method] += 1

                # jeśli przypadek skrajny o mniejszym sąsiedztwie niż zakładamy (+/-3) - interpolacja
                else:
                    f = interpolate.interp1d(inds[nan_values], RR_with_nan[nan_values], bounds_error=False)
                    if np.isnan(obj.examination.RR_intervals[val].value):
                        # Apply cubic spline interpolation based on the index associated with the interval
                        obj.examination.RR_intervals[val].value = f(val)
                        obj.examination.RR_intervals[val].correction_methods["linear interpolation"] += 1

            # if any nans left (happen if there are many nans near each other or at the beggining/end - interpolate)
            RR_with_nan_new = np.array([interval.value for interval in obj.examination.RR_intervals])
            f = interpolate.interp1d(inds[~np.isnan(RR_with_nan_new)], RR_with_nan_new[~np.isnan(RR_with_nan_new)], bounds_error=False)
            for i, interval in enumerate(obj.examination.RR_intervals):
                # Check if the interval value needs correction (e.g., if it's NaN)
                if np.isnan(interval.value):
                    # Apply linear interpolation based on the index associated with the interval
                    interval.value = f(i)
                    interval.correction_methods["linear interpolation"] += 1


        # pętla usuwająca wartości NAN z początku badania - te wartości nie mogły zostać zinterpolowane
        while np.isnan(obj.examination.RR_intervals[0].value):
            obj.examination.RR_intervals.pop(0)
            # jesli usunieto 1. element - zaktualizować indeksy
            for key in obj.examination.artifacts.keys():
                obj.examination.artifacts[key] = [x - 1 for x in obj.examination.artifacts[key]]
        
        # pętla usuwająca wartości NAN z końca badania
        while np.isnan(obj.examination.RR_intervals[-1].value):
            obj.examination.RR_intervals.pop(-1)
            for key in obj.examination.artifacts.keys():
                if len(obj.examination.RR_intervals) in obj.examination.artifacts[key]:
                    obj.examination.artifacts[key].remove(len(obj.examination.RR_intervals))

        obj.examination.RR = np.array([int(element.value) for element in obj.examination.RR_intervals])
        for key in obj.examination.artifacts.keys():
            for i in idx:
                if i in obj.examination.artifacts[key]:
                    obj.examination.artifacts[key].remove(i)
        
        obj.examination.RR  = np.array([interval.value for interval in obj.examination.RR_intervals])
        return deleted
    else:
        return np.array([])

