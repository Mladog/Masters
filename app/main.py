"""
Moduł odpowiedzialny za uruchomienie aplikacji
"""

"""
TODO:

1) Dodanie funkcji do poprawiania artefaktów metodą Marcela (tylko próbki z przeszłości, liczba dostosowywalna)
2) Dodanie obsługi .xlsx .csv
3) Zmienić komentarze na j. angielski
4) Korekcja raportu

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
