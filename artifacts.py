"""
Moduł odpowiedziany za automatyczne wyznaczanie artefaktów
"""
import numpy as np

def find_art1(RR):
    """
    funkcja do wyszukiwania artefaktów typu 1
    """
    # obliczone różnice między obecnym i poprzednim interwałem
    d_prev = [1 if abs(d) > 200 else 0 for d in RR[1:]- RR[:-1]]
    d_prev.insert(0, 0)
    # obliczone różnice między obecnym i nstępnym interwałem
    d_next = [1 if abs(d) > 200 else 0 for d in RR[:-1]-RR[1:]]
    d_next.insert(-1, 0)

    # wyszukanie miejsc, w których próbka ma 20 ms rożnicy między zarówno
    # poprzednim jak i następnym interwałem
    final_list = [sum(value) for value in zip(d_prev, d_next)]
    idx = np.where(np.array(final_list) == 2)[0]

    return idx