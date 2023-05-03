"""
Moduł odpowiedzialny za uruchomienie aplikacji
"""

"""
TODO:
1) doczytać o warunkach zaliczenia artefaktu do zbioru 2/3 (też na potem)
2) przyczepić legendę inaczej (na potem)
3) test stacjonarności HRV
4) opcja zaznaczenia pierwszego i ostatniego bitu klinięciem
5) uzupełnienie HRV o te, które chce Kuba (czekam na maila)
6) porównanie wszystkich param. z PyBiosem
7) crush testy
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
