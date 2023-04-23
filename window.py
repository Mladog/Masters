"""
module containing Window definition
"""

import numpy as np
import pyqtgraph as pg
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6 import QtCore

from artifacts import find_art1, find_art2, find_art3, remove_artifacts
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
        self.chosen_artifacts = []
        self.method = "lin"
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
        self.update_plot()

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
            diff_y = np.abs(self.examination.RR - mouse_point.y())
            diff_x = np.abs(np.array(range(len(self.examination.RR))) - mouse_point.x())
            idx = (np.abs(diff_x + diff_y)).argmin()
            self.coords_x = idx
            add_point_to_graph(self)

    def update_hrv_params(self):
        new_params = create_hrv_summary(count_hrv(self.examination))
        self.hrv_label.setText(new_params)
   
    def choose_artifact(self):
        """
        funkcja oznaczająca nowy artefakt
        """
        for b in [self.t1, self.t2, self.t3]:
            if b.isChecked() == True:
                self.toggle_button_selected = b.text()
        self.examination.artifacts["Manual " + self.toggle_button_selected].append(self.coords_x)
        self.plot_artifacts()

    def del_artifact(self, points_to_del):
        """ 
        funkcja usuwająca wybrane artefakty
        """
        for el in self.examination.artifacts.keys():
            if len(points_to_del) > 0:
                if len(points_to_del) == 1:
                    self.examination.artifacts[el].remove(point)
                else:
                    for point in points_to_del:
                        if point in self.examination.artifacts[el]:
                            self.examination.artifacts[el].remove(point)
        #self.plot_artifacts()

    def auto_detect(self):
        self.examination.artifacts["Auto T1"] = find_art1(self)
        self.examination.artifacts["Auto T2"] = find_art2(self)
        self.examination.artifacts["Auto T3"] = find_art3(self)
        self.plot_artifacts()

    def delete_chosen_artifacts(self):
        self.chosen_artifacts = [chbx.text() for chbx in self.checkbox_list if chbx.isChecked()]
        if len(self.chosen_artifacts) > 0:
            to_del, _ = remove_artifacts(self)
            #self.examination.get_RR_vect()
            print(to_del)
            self.del_artifact(to_del)
            self.update_plot()
            self.plot_artifacts()

    def update_plot(self):
        for p in [self.plot_art, self.p3, self.plot_cursor, self.legend]:
            p.clear()
        
        self.plot_label.setXRange(-100, len(self.examination.RR)+150, padding=0)
        self.plot_label.setYRange(-100, max(self.examination.RR)+150, padding=0)
        self.RRs = pg.PlotCurveItem(self.examination.RR, pen='b')
        self.plot_art.addItem(self.RRs)
        self.update_hrv_params()
        
    def plot_artifacts(self):
        self.points_T1_auto = pg.ScatterPlotItem(self.examination.artifacts["Auto T1"], 
                                       self.examination.RR[self.examination.artifacts["Auto T1"]],
                                       brush=pg.mkBrush(255, 214, 77, 120), hoverable=True)
        self.points_T2_auto = pg.ScatterPlotItem(self.examination.artifacts["Auto T2"], 
                                       self.examination.RR[self.examination.artifacts["Auto T2"]],
                                       brush=pg.mkBrush(0, 255, 0, 120), hoverable=True)
        self.points_T3_auto = pg.ScatterPlotItem(self.examination.artifacts["Auto T3"], 
                                       self.examination.RR[self.examination.artifacts["Auto T3"]],
                                       brush=pg.mkBrush(0, 0, 255, 120), hoverable=True)

        self.points_T1_manual = pg.ScatterPlotItem(self.examination.artifacts["Manual T1"], 
                                       self.examination.RR[self.examination.artifacts["Manual T1"]],
                                       brush=pg.mkBrush(255, 127, 80, 255), hoverable=True)
        self.points_T2_manual = pg.ScatterPlotItem(self.examination.artifacts["Manual T2"], 
                                       self.examination.RR[self.examination.artifacts["Manual T2"]],
                                       brush=pg.mkBrush(67, 94, 82, 255), hoverable=True)
        self.points_T3_manual = pg.ScatterPlotItem(self.examination.artifacts["Manual T3"], 
                                       self.examination.RR[self.examination.artifacts["Manual T3"]],
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
