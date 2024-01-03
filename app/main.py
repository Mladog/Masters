"""
Moduł odpowiedzialny za uruchomienie aplikacji
"""

"""
TODO:

1) Dodanie obsługi .xlsx
2) Korekcja raportu (uwzględnić shorty)
3) Zmienić komentarze na j. angielski

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
