"""
Moduł służący utworzeniu układu wykresu oraz parametrów RR
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel
from graph import create_graph

def create_RR_layout(obj):
    """
    funkcja odpowiedzialna za rozmieszczenie przycisków
    """
    # utworzenie wykresu
    obj.graphWidget = create_graph(obj)
    obj.RR_layout.addWidget(obj.graphWidget)

    obj.hrv_label = QLabel("oczekiwanie na wczytanie \nsygnału")
    obj.hrv_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    obj.RR_layout.addWidget(obj.hrv_label)