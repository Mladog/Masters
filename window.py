"""
module containing Window definition
"""

import numpy as np
import pyqtgraph as pg
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6 import QtCore


from artifacts import find_art1
from examination import Examination
from hrv import count_hrv, create_hrv_summary
from widgets import create_widgets


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
        # zmienna przechowująca aktywne elementy wykresu
        self.active_plot_items = []
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
        self.p2.clear()
        self.p1.setXRange(-100, len(self.examination.RR)+150, padding=0)
        self.p1.setYRange(-100, max(self.examination.RR)+150, padding=0)
        self.p2_plot = pg.PlotCurveItem(self.examination.RR, pen='b')
        self.p2.addItem(self.p2_plot)
        self.update_hrv_params()
        
        #self.p3.clear()

    def mouse_moved(self, evt):
        """
        funkcja wychwytująca ruch myszki w obrębie wykresu
        """
        vb = self.graphWidget.plotItem.vb
        if self.graphWidget.sceneBoundingRect().contains(evt):
            mouse_point = vb.mapSceneToView(evt)
            self.label.setHtml(f"<p style='color:white'>X: {mouse_point.x()} <br> Y: {mouse_point.y()}</p>")

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
        if b.isChecked == True:
            print(b.text() + "is selected")
        
        return b.text()
    
    def choose_artifact(self):
        """
        """
        for b in [self.t1, self.t2, self.t3, self.t4, self.t5, self.t6]:
            if b.isChecked() == True:
                self.toggle_button_selected = b.text()
        print(self.toggle_button_selected)

    def auto_detect(self):
        self.artifacts["T1"] = find_art1(self.examination.RR)
        # przenieść to do modułu graph
        points_T1 = pg.ScatterPlotItem(self.artifacts["T1"], 
                                       self.examination.RR[self.artifacts["T1"]],
                                       brush=pg.mkBrush(219, 0, 0, 120), hoverable=True)
        #points_T1.addLegend('artefakt 1')
        self.graphWidget.addItem(points_T1)

        self.legend.addItem(points_T1, 'artefakt1')
        self.legend.setPos(self.legend.mapFromItem(self.legend, QtCore.QPointF(0, max(self.examination.RR))))