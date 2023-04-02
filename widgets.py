"""
window_widgets
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton

from wykres import create_graph
from buttons_layout import create_blayout

def create_widgets(obj) -> None:
    """
    adding widgets to main window
    """
    label = QLabel("Aplikacja do wyłapywania artefaktów")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    obj.main_layout.addWidget(label)
    file_btn = QPushButton(obj)
    file_btn.setText("Open file dialog")
    obj.main_layout.addWidget(file_btn)
    file_btn.clicked.connect(obj.open_dialog)
    create_graph(obj)
    obj.main_layout.addWidget(obj.graphWidget)
    btn = QPushButton(obj)
    btn.setText("guzik")
    obj.main_layout.addWidget(btn)
    obj.main_layout.addLayout(obj.buttons_layout)
    #create_blayout(obj)
