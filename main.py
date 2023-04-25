"""
Moduł odpowiedzialny za uruchomienie aplikacji
"""

"""
TODO:
1) doczytać o warunkach zaliczenia artefaktu do zbioru 2/3
2) metoda usuwająca artefakt z sygnału (del)
3) dołożenie artefaktu "inne"
4) test stacjonarności HRV
5) poprawność wyznaczania HRV!!!

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
