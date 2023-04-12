"""
moduł odpowiedzialny za utworzenie widgetów
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QRadioButton

from RR_layout import create_RR_layout
from buttons_layout import create_buttons_layout

def create_widgets(obj) -> None:
    """
    dodanie widgetów 
    """

    # utworzenie etykiety z wyśrodkowanym tekstem
    # oraz dodanie jej do głównego układu
    obj.label = QLabel("Aplikacja do wyłapywania artefaktów")
    obj.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    obj.main_layout.addWidget(obj.label)

    # utworzenie przycisku odpowiedzialnego za możliwość 
    # wczytania nowego pliku
    obj.file_btn = QPushButton(obj)
    obj.file_btn.setText("Wczytaj plik")
    obj.main_layout.addWidget(obj.file_btn)
    obj.file_btn.clicked.connect(obj.open_dialog)

    # dodanie układu RR
    create_RR_layout(obj)
    obj.main_layout.addLayout(obj.RR_layout)

    # dodanie układu przycisków
    obj.main_layout.addLayout(obj.buttons_layout)
    
    # utworzenie przycisków radiowych do oznaczenia typu artefaktu
    obj.t1 = QRadioButton("T1", obj)
    obj.t2 = QRadioButton("T2", obj)
    obj.t3 = QRadioButton("T3", obj)
    obj.t4 = QRadioButton("T4", obj)
    obj.t5 = QRadioButton("T5", obj)
    obj.t6 = QRadioButton("T6", obj)
    
    # utworzenie układów
    create_buttons_layout(obj)
