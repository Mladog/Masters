"""
module containing Window definition
"""

import numpy as np
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFileDialog, QWidget

from widgets import create_widgets
from examination import Examination
from hrv import create_hrv_summary, count_hrv


class Window(QWidget):
    """
    main window of app
    """
    def __init__(self):
        super().__init__()
        # dostosowanie wielkości okna
        self.resize(700, 500)
        # tytuł aplikacji
        self.setWindowTitle("Artefakty")
        # ikona aplikacji (TODO)
        self.setWindowIcon(QIcon("icon.jpg"))
        # ścieżka do obsługiwanego pliku
        self.fname = ""
        # badanie
        self.examination = Examination()
        # główny układ aplikacji
        self.main_layout = QVBoxLayout()
        # układ wertykalny
        self.vlayout = QVBoxLayout()
        # układ przycisków
        self.buttons_layout = QHBoxLayout()
        # układ wykresu i parametrów
        self.RR_layout = QHBoxLayout()
        # ustawienie głównego układu
        self.setLayout(self.main_layout)
        # stworzenie początkowych widgetów
        create_widgets(self)

    def open_dialog(self):
        """
        funkcja odpowiedzialna za wybór pliku z okna dialogowego
        """
        dialog = QFileDialog()
        dialog.setNameFilter(".csv") #to nie działa
        self.fname, _ = dialog.getOpenFileName(
            self,
            "Open File",
            "examination.xls",
        )
        self.examination = Examination(self.fname)
        self.graphWidget.plot(self.examination.RR)
        self.update_hrv_params()

    def mouse_moved(self, evt):
        """
        funkcja wychwytująca ruch myszki w obrębie wykresu
        """
        vb = self.graphWidget.plotItem.vb
        if self.graphWidget.sceneBoundingRect().contains(evt):
            mouse_point = vb.mapSceneToView(evt)
            self.label.setHtml(f"<p style='color:white'>X： {mouse_point.x()} <br> Y: {mouse_point.y()}</p>")

    def mouse_clicked(self, evt):
        """
        funkcja wychwytująca kliknięcie myszki w obrębie wykresu
        """
        vb = self.graphWidget.plotItem.vb
        scene_coords = evt.scenePos()
        if self.graphWidget.sceneBoundingRect().contains(scene_coords):
            mouse_point = vb.mapSceneToView(scene_coords)
            print(f'clicked plot X: {mouse_point.x()}, Y: {mouse_point.y()}, event: {evt}')

    def update_hrv_params(self):
        new_params = create_hrv_summary(count_hrv(self.examination))
        self.hrv_label.setText(new_params)

    def btnstate(self, b):
        """
        funckja zwracająca stan przycisku 
        """
        
        if b.text() == "Button1":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")
                
        if b.text() == "Button2":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")