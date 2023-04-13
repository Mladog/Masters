"""
module containing Window definition
"""

import numpy as np
import pyqtgraph as pg
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6 import QtCore

from artifacts import find_art1, find_art2, find_art3
from examination import Examination
from hrv import count_hrv, create_hrv_summary
from widgets import create_widgets
from new_graph import add_point_to_graph


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
        # układ początkowej linii
        self.first_row = QHBoxLayout()
        # układ przycisków
        self.r_buttons_layout = QHBoxLayout()
        self.c_buttons_layout = QHBoxLayout()
        # układ wykresu i parametrów
        self.RR_layout = QHBoxLayout()
        # ustawienie głównego układu
        self.setLayout(self.main_layout)
        # zmienna przechowująca aktywne elementy wykresu //chyba nie jest dłużej potrzebne
        self.active_plot_items = []
        # zmienne przechowująca współrzędne pierwszego punktu do oznaczenia
        self.coords_x = None
        self.coords_y = None
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
        for p in [self.p2, self.p3, self.plot_cursor, self.legend]:
            p.clear()
        
        self.p1.setXRange(-100, len(self.examination.RR)+150, padding=0)
        self.p1.setYRange(-100, max(self.examination.RR)+150, padding=0)
        self.p2_plot = pg.PlotCurveItem(self.examination.RR, pen='b')
        self.p2.addItem(self.p2_plot)
        self.update_hrv_params()

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
            diff_y = np.abs(self.examination.RR - mouse_point.y())
            diff_x = np.abs(np.array(range(len(self.examination.RR))) - mouse_point.x())
            idx = (np.abs(diff_x + diff_y)).argmin()
            self.coords_x = idx
            print(self.coords_x, self.examination.RR[idx])
            add_point_to_graph(self)

    def update_hrv_params(self):
        new_params = create_hrv_summary(count_hrv(self.examination))
        self.hrv_label.setText(new_params)

    """def btnstate(self, b):
        if b.isChecked == True:
            print(b.text() + "is selected")
        
        return b.text()"""
    
    def choose_artifact(self):
        """
        funkcja oznaczająca nowy artefakt
        """
        for b in [self.t1, self.t2, self.t3]:
            if b.isChecked() == True:
                self.toggle_button_selected = b.text()
        self.examination.artifacts[self.toggle_button_selected + "_manual"].append(self.coords_x)
        self.plot_artifacts()

    def del_artifact(self):
        """ 
        funkcja usuwająca zaznaczony nadmiarowo epizod
        """
        for el in self.examination.artifacts.keys():
            if self.coords_x in self.examination.artifacts[el]:
                self.examination.artifacts[el].remove(self.coords_x)
        self.plot_artifacts()

    def auto_detect(self):
        self.examination.artifacts["T1_auto"] = find_art1(self)
        self.examination.artifacts["T2_auto"] = find_art2(self)
        self.examination.artifacts["T3_auto"] = find_art3(self)
        self.plot_artifacts()
        
    def plot_artifacts(self):
        self.points_T1_auto = pg.ScatterPlotItem(self.examination.artifacts["T1_auto"], 
                                       self.examination.RR[self.examination.artifacts["T1_auto"]],
                                       brush=pg.mkBrush(255, 214, 77, 120), hoverable=True)
        self.points_T2_auto = pg.ScatterPlotItem(self.examination.artifacts["T2_auto"], 
                                       self.examination.RR[self.examination.artifacts["T2_auto"]],
                                       brush=pg.mkBrush(0, 255, 0, 120), hoverable=True)
        self.points_T3_auto = pg.ScatterPlotItem(self.examination.artifacts["T3_auto"], 
                                       self.examination.RR[self.examination.artifacts["T3_auto"]],
                                       brush=pg.mkBrush(0, 0, 255, 120), hoverable=True)

        self.points_T1_manual = pg.ScatterPlotItem(self.examination.artifacts["T1_manual"], 
                                       self.examination.RR[self.examination.artifacts["T1_manual"]],
                                       brush=pg.mkBrush(255, 127, 80, 255), hoverable=True)
        self.points_T2_manual = pg.ScatterPlotItem(self.examination.artifacts["T2_manual"], 
                                       self.examination.RR[self.examination.artifacts["T2_manual"]],
                                       brush=pg.mkBrush(67, 94, 82, 255), hoverable=True)
        self.points_T3_manual = pg.ScatterPlotItem(self.examination.artifacts["T3_manual"], 
                                       self.examination.RR[self.examination.artifacts["T3_manual"]],
                                       brush=pg.mkBrush(82, 67, 94, 255), hoverable=True)
        self.p3.clear()
        for el in [self.points_T1_auto, self.points_T2_auto, self.points_T3_auto,
                   self.points_T1_manual, self.points_T2_manual, self.points_T3_manual]:
            self.p3.addItem(el)

        # ustawienia legendy 
        self.legend.clear()
        self.legend.addItem(self.points_T1_auto, 'auto T1')
        self.legend.addItem(self.points_T2_auto, 'auto T2')
        self.legend.addItem(self.points_T3_auto, 'auto T3')
        self.legend.addItem(self.points_T1_manual, 'manual T1')
        self.legend.addItem(self.points_T2_manual, 'manual T2')
        self.legend.addItem(self.points_T3_manual, 'manual T3')
        self.legend.setPos(self.legend.mapFromItem(self.legend, QtCore.QPointF(0, max(self.examination.RR))))
