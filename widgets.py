"""
window_widgets
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton

from wykres import create_graph

def create_widgets(obj, layout) -> None:
    """
    adding widgets to main window
    """
    label = QLabel("Aplikacja do wyłapywania artefaktów")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label)
    btn = QPushButton(obj)
    btn.setText("Open file dialog")
    layout.addWidget(btn)
    btn.clicked.connect(obj.open_dialog)
    create_graph(obj)
    layout.addWidget(obj.graphWidget)
