"""
module responsible for App running
"""
import sys

from PyQt6.QtWidgets import QApplication

from window import Window

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
