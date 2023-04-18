"""
Moduł odpowiedzialny za uruchomienie aplikacji
"""

"""
TODO:
1) program nie działa jeśli kliknę wyznaczanie autom. atrybutów przed wczytaniem plików
2) jedna funkcja do wyznaczania wszystkich rodzajów artefaktów
3) dołożenie artefaktu "inne"
4) test stacjonarności HRV
5) interpolacja kilkoma metodami
    i) usunięcie próbki
    ii) interpolacja liniowa
    iii) interpolacja sześcienna splajnu
    iv) ?
6) możliwość zaznaczania wielokrotnego
"""


import sys

from PyQt6.QtWidgets import QApplication

from window import Window

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
