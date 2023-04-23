"""
moduł odpowiedzialny za utworzenie widgetów
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QCheckBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QRadioButton)

from buttons_layout import create_buttons_layout
from RR_layout import create_RR_layout


def create_widgets(obj) -> None:
    """
    dodanie widgetów 
    """

    # utworzenie etykiety z wyśrodkowanym tekstem
    # oraz dodanie jej do głównego układu
    obj.label = QLabel("Aplikacja do wyłapywania artefaktów")
    obj.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    obj.first_row.addWidget(obj.label)
    obj.main_layout.addLayout(obj.first_row)

    # utworzenie przycisku odpowiedzialnego za możliwość 
    # wczytania nowego pliku
    obj.file_btn = QPushButton(obj)
    obj.file_btn.resize(100, 50)
    obj.file_btn.setText("Wczytaj plik")
    obj.first_row.addWidget(obj.file_btn)
    obj.file_btn.clicked.connect(obj.open_dialog)

    # utworzenie opcji do wpisania ręcznego
    obj.textbox_layout = QHBoxLayout()
    obj.label_art1 = QLabel("T1: Rozbieżność w jednym przedziale [ms]")
    obj.label_art2 = QLabel("T2: Długi interwał po krótkim [ms]")
    obj.label_art3 = QLabel("T3: Krótki interwał po długim [ms]")
    obj.textbox_art1 = QLineEdit(obj)
    obj.textbox_art1.setText("200")
    obj.textbox_art2 = QLineEdit(obj)
    obj.textbox_art2.setText("400")
    obj.textbox_art3 = QLineEdit(obj)
    obj.textbox_art3.setText("400")
    for el in [obj.label_art1, obj.textbox_art1,
               obj.label_art2, obj.textbox_art2,
               obj.label_art3, obj.textbox_art3]:
        obj.textbox_layout.addWidget(el)
    
    obj.main_layout.addLayout(obj.textbox_layout)

    obj.auto_art = QPushButton(obj)
    obj.auto_art.setText("Wyznacz artefakty automatycznie")
    obj.auto_art.clicked.connect(lambda:obj.auto_detect())
    obj.main_layout.addWidget(obj.auto_art)
    # dodanie układu RR
    create_RR_layout(obj)
    obj.main_layout.addLayout(obj.RR_layout)

    # dodanie układu przycisków
    obj.main_layout.addLayout(obj.r_buttons_layout)
    obj.main_layout.addLayout(obj.c_buttons_layout)
    
    # utworzenie przycisków radiowych do oznaczenia typu artefaktu
    obj.t1 = QRadioButton("T1", obj)
    obj.t2 = QRadioButton("T2", obj)
    obj.t3 = QRadioButton("T3", obj)

    # utworzenie przycisków do usuwania grup artefaktów
    obj.t1_auto = QCheckBox("T1_auto")
    obj.t2_auto = QCheckBox("T2_auto")
    obj.t3_auto = QCheckBox("T3_auto")
    obj.t1_man = QCheckBox("T1_manual")
    obj.t2_man = QCheckBox("T2_manual")
    obj.t3_man = QCheckBox("T3_manual")
    obj.current = QCheckBox("Obecne zaznaczenie")
    obj.checkbox_list = [obj.t1_auto, obj.t2_auto, obj.t3_auto,
                         obj.t1_man, obj.t2_man, obj.t3_man,
                         obj.current]
    
    # utworzenie układów
    create_buttons_layout(obj)
