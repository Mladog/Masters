"""
Moduł odpowiedzialny za uruchomienie aplikacji
"""

"""
TODO:
1) doczytać o warunkach zaliczenia artefaktu do zbioru 2/3
2) dodanie opcji moving avg (done) i NPI w metodach korekcji - chwilowo za trudne, mogę do tego wrócić na koniec
3) przyczepić legendę inaczej
4) test stacjonarności HRV
5) parametry HRV i info o skorygowanych artefaktach każdego typu do pliku
6) opcja zaznaczenia pierwszego i ostatniego bitu, który ma być brany pod uwagę w analizie hrv
    i) możliwość wpisania nr próbki
    ii) możliwość kliknięcia próbki
7) uzupełnienie HRV o te, które chce Kuba
8) porównanie wszystkich param. z PyBiosem
9) opcja białego wykresu dla Marcela
10) crush testy

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
