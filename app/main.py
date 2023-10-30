"""
Moduł odpowiedzialny za uruchomienie aplikacji
"""

"""
TODO:

+1) Zmiana na j. ang
-2) Dodanie funkcji do poprawiania artefaktów w oknie
+3) Dodanie funkcji do poprawiania artefaktów metodą Marcela (3 z przeszłości + 1 z przyszłości)
-4) Zmiana sposobu podliczania artefaktów (próbka sygnału to element klasy?)
-5) Zmienic kod tak, aby obslugiwal inne pliki niż Kuby

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
