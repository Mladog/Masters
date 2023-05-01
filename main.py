"""
Moduł odpowiedzialny za uruchomienie aplikacji
"""

"""
TODO:
1) doczytać o warunkach zaliczenia artefaktu do zbioru 2/3
2) przyczepić legendę inaczej (na potem)
3) test stacjonarności HRV
4) parametry HRV do pliku
5) opcja zaznaczenia pierwszego i ostatniego bitu, który ma być brany pod uwagę w analizie hrv
    i) możliwość wpisania nr próbki
    ii) możliwość kliknięcia próbki
6) uzupełnienie HRV o te, które chce Kuba
7) porównanie wszystkich param. z PyBiosem
8) opcja białego wykresu dla Marcela
9) crush testy
"""


import sys

from PyQt6.QtWidgets import QApplication

from window import Window
import warnings
warnings.filterwarnings("ignore")

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
