
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from wykres import create_graph
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(700, 500)
        self.setWindowTitle("Artefakty")
        self.setWindowIcon(QIcon("icon.jpg"))
 
        layout = QVBoxLayout()
        self.setLayout(layout)
 
        label = QLabel("Aplikacja do wyłapywania artefaktów")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        create_graph(self)
        layout.addWidget(self.graphWidget)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())


