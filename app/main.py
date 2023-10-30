"""
Moduł odpowiedzialny za uruchomienie aplikacji
"""

"""
TODO:

1) Dodanie funkcji do poprawiania artefaktów w oknie
2) Dodanie funkcji do poprawiania artefaktów metodą Marcela (tylko próbki z przeszłości, liczba dostosowywalna)
3) Zmiana sposobu podliczania artefaktów (próbka sygnału to element klasy?)
4) Dodanie obsługi .xlsx .csv
5) Zmienić komentarze na j. angielski

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
