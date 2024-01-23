"""
moduł odpowiedzialny za utworzenie widgetów
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QCheckBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QRadioButton, QButtonGroup,
                             QComboBox)

from buttons_layout import create_buttons_layout
from RR_layout import create_RR_layout
from hrv_options import initialize_hrv_options


def create_widgets(obj) -> None:
    """
    dodanie widgetów 
    """

    # utworzenie etykiety z wyśrodkowanym tekstem
    # oraz dodanie jej do głównego układu
    obj.label = QLabel("Load file with extensions .txt, .csv or xls:")
    obj.first_row.addWidget(obj.label, alignment=Qt.AlignmentFlag.AlignRight)
    obj.main_layout.addLayout(obj.first_row)

    # utworzenie przycisku odpowiedzialnego za możliwość 
    # wczytania nowego pliku
    obj.file_btn = QPushButton(obj)
    obj.file_btn.resize(100, 50)
    obj.file_btn.setText("Load file")
    obj.first_row.addWidget(obj.file_btn)
    obj.file_btn.clicked.connect(obj.open_dialog)

    # utworzenie opcji do wpisania ręcznego
    obj.textbox_layout = QHBoxLayout()
    obj.label_art1 = QLabel("T1: Difference in one section [ms]")
    obj.label_art2 = QLabel("T2: Long interval before short one [ms]")
    obj.label_art3 = QLabel("T3: Short interval before long one [ms]")
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
    
    # dodanie układu hrv
    obj.main_layout.addLayout(obj.hrv_options_layout_1)
    obj.main_layout.addLayout(obj.hrv_options_layout_2)
    initialize_hrv_options(obj)


    obj.auto_art = QPushButton(obj)
    obj.auto_art.setText("Artifacts auto-finding")
    obj.auto_art.clicked.connect(lambda:obj.auto_detect())
    obj.main_layout.addWidget(obj.auto_art)

    # dodanie układu RR
    create_RR_layout(obj)
    obj.main_layout.addLayout(obj.RR_layout)

    # dodanie układu przycisków
    obj.main_layout.addLayout(obj.r_buttons_layout)
    obj.main_layout.addLayout(obj.c_buttons_layout)
    obj.main_layout.addLayout(obj.m_buttons_layout)
    
    # utworzenie przycisków radiowych do oznaczenia typu artefaktu
    obj.t1 = QRadioButton("T1", obj)
    obj.t2 = QRadioButton("T2", obj)
    obj.t3 = QRadioButton("T3", obj)
    obj.diff = QRadioButton("other", obj)

    # utworzenie przycisków radiowych do wyboru metody usunięcia artefaktów
    obj.m1 = QRadioButton("linear interpolation", obj)
    obj.m2 = QRadioButton("cubic splain", obj)
    obj.m3 = QRadioButton("deletion", obj)
    obj.m4 = QRadioButton("moving average", obj)
    obj.m5 = QRadioButton("pre mean", obj)

    # przycisk definijący ilosc interwałów przed artefaktem
    obj.pre_mean_count = QComboBox()
    obj.pre_mean_count.addItems(["2", "3", "4", "5", "6", "7", "8", "9", "10"])
    obj.pre_mean_count.setCurrentText("4")

    # utworzenie przycisków do usuwania grup artefaktów
    obj.Tarvainen = QCheckBox("Tarvainen")
    obj.t1_auto = QCheckBox("T1_auto")
    obj.t2_auto = QCheckBox("T2_auto")
    obj.t3_auto = QCheckBox("T3_auto")
    obj.t1_man = QCheckBox("T1_manual")
    obj.t2_man = QCheckBox("T2_manual")
    obj.t3_man = QCheckBox("T3_manual")
    obj.diff_man = QCheckBox("other_manual")
    obj.checkbox_list = [obj.Tarvainen, obj.t1_auto, obj.t2_auto, obj.t3_auto,
                         obj.t1_man, obj.t2_man, obj.t3_man, obj.diff_man]
    
    # utworzenie układów
    create_buttons_layout(obj)
