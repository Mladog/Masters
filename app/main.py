"""
Moduł odpowiedzialny za uruchomienie aplikacji
"""

"""
TODO:

1) test stacjonarności HRV - w teorii jest
2) opcja zaznaczenia pierwszego i ostatniego bitu klinięciem
3) uzupełnienie HRV o te, które chce Kuba (czekam na maila)
4) crush testy
5) poprawić przyczepienie legendy
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
