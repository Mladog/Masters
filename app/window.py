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
from view_manager import initialize_views

class Window(QWidget):
    """
    Główne okno aplikacji
    """
    def __init__(self):
        super().__init__()
        # dostosowanie wielkości okna
        self.resize(700, 500)
        # tytuł aplikacji
        self.setWindowTitle("Artifacts")
        # ścieżka do obsługiwanego pliku
        self.fname = ""
        # badanie
        self.examination = Examination()
        initialize_views(self)
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
        self.fname, _ = dialog.getOpenFileName(
            self,
            "Open File",
        )
        if self.fname:
            self.examination = Examination(self.fname)
            self.h1.setChecked(True)
            self.coords_x = None
            self.update_plot()
            # wpisanie numerów pierwszego i ostatniego interwału do textboxów 
            self.textbox_start.setText("0")
            self.textbox_end.setText(f"{str(len(self.examination.RR)-1)}")

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
        """
        funkcja odpowiadajaca za przeliczenie parametrow hrv i wyswietlenie nowych wartosci
        """
        new_params = create_hrv_summary(count_hrv(self))
        self.hrv_label.setText(new_params)
   
    def choose_artifact(self):
        """
        funkcja oznaczająca nowy artefakt
        """
        if self.coords_x:
            for b in [self.t1, self.t2, self.t3, self.diff]:
                if b.isChecked() == True:
                    self.toggle_button_selected = b.text()
            self.examination.artifacts[self.toggle_button_selected + "_manual"].append(self.coords_x)
            self.plot_artifacts()

    def del_artifact(self, points_to_del):
        """ 
        funkcja usuwająca wybrane artefakty
        """
        for key in self.examination.artifacts.keys():
            if len(points_to_del) > 0:
                for point in points_to_del:
                    if point in self.examination.artifacts[key]:
                        self.examination.artifacts[key].remove(point)
        
        self.plot_artifacts()

    def save_data(self):
        """
        funkcja odpowiedzialna za zapis danych
        """
        dialog = QFileDialog()
        file_name = f"{self.examination.path[:-4]}_clean" if self.h1.isChecked() == True else f"{self.examination.path[:-4]}_short_clean"
        fname, _ = dialog.getSaveFileName(
            self,
            "Open File",
            f"{file_name}",
        )
        if len(fname)> 0:
            if ".txt" in fname:
                fname = fname[:-4]
            if self.h1.isChecked() == True:
                self.examination.save_to_txt(f"{fname}.txt")
            else:
                self.examination.save_to_txt(f"{fname}.txt", range=[self.exam_start,self.exam_stop])
            with open(f'{fname}_stats.txt', 'w') as f:
                f.write(f"number of removed artifacts: {self.examination.original_len - len(self.examination.RR_intervals)}\n")
                f.write(f"number of corrected artifacts: {sum(interval.artifact for interval in self.examination.RR_intervals if interval.artifact)}")
                for key in self.examination.RR_intervals[0].correction_methods.keys():
                    sum_pre_mean_artifact_true = sum(interval.correction_methods[key] for interval in self.examination.RR_intervals if interval.artifact)
                    f.write("%s: %s\n" % (key, sum_pre_mean_artifact_true))
                    
                f.write("\nHRV parameters:\n")
                f.write(self.hrv_label.text())

    def auto_detect(self):
        """
        funkcja znajdujaca artefakty automatycznie i wykreslajaca je na wykresie
        """
        # warunek wczytania badania
        if len(self.examination.RR) > 0:
            self.examination.artifacts["T1_auto"] = find_art1(self)
            self.examination.artifacts["T2_auto"] = find_art2(self)
            self.examination.artifacts["T3_auto"] = find_art3(self)
            self.plot_artifacts()

    def delete_chosen_artifacts(self):
        """
        funkcja odpowiedzialna za usuwanie wybranych artefaktow
        """
        self.chosen_artifacts = [chbx.text() for chbx in self.checkbox_list if chbx.isChecked()]
        if len(self.chosen_artifacts) > 0:
            to_del = remove_artifacts(self)
            self.update_plot()
            self.del_artifact(to_del)
            self.update_hrv_params()
            self.examination.deleted_artifacts += len(to_del)

    def update_plot(self):
        """
        funkcja aktualizująca wykres po zmianie jego parametrow
        """
        for p in [self.plot_art, self.p3, self.plot_cursor, self.legend]:
            p.clear()
        
        self.plot_label.setXRange(-100, len(self.examination.RR)+150, padding=0)
        self.plot_label.setYRange(-100, max(self.examination.RR)+150, padding=0)
        self.RRs = pg.PlotCurveItem(self.examination.RR, pen='b')
        self.plot_art.addItem(self.RRs)
        self.update_hrv_params()
        
    def plot_artifacts(self):
        """
        funkcja odpowiedzialna za wykreslanie artefaktów na wykresie
        """
        #self.exam_start
        #self.exam_stop
        # okreslenie miejsc występowania artefaktów
        self.points_T1_auto = pg.ScatterPlotItem(self.examination.artifacts["T1_auto"], 
                                       self.examination.RR[self.examination.artifacts["T1_auto"]],
                                       brush=pg.mkBrush(255, 255, 0, 255), hoverable=True)
        self.points_T2_auto = pg.ScatterPlotItem(self.examination.artifacts["T2_auto"], 
                                       self.examination.RR[self.examination.artifacts["T2_auto"]],
                                       brush=pg.mkBrush(0, 255, 0, 255), hoverable=True)
        self.points_T3_auto = pg.ScatterPlotItem(self.examination.artifacts["T3_auto"], 
                                       self.examination.RR[self.examination.artifacts["T3_auto"]],
                                       brush=pg.mkBrush(255, 0, 128, 255), hoverable=True)

        self.points_T1_manual = pg.ScatterPlotItem(self.examination.artifacts["T1_manual"], 
                                       self.examination.RR[self.examination.artifacts["T1_manual"]],
                                       brush=pg.mkBrush(255, 127, 80, 255), hoverable=True)
        self.points_T2_manual = pg.ScatterPlotItem(self.examination.artifacts["T2_manual"], 
                                       self.examination.RR[self.examination.artifacts["T2_manual"]],
                                       brush=pg.mkBrush(0, 255, 255, 255), hoverable=True)
        self.points_T3_manual = pg.ScatterPlotItem(self.examination.artifacts["T3_manual"], 
                                       self.examination.RR[self.examination.artifacts["T3_manual"]],
                                       brush=pg.mkBrush(102, 0, 204, 255), hoverable=True)

        self.points_diff = pg.ScatterPlotItem(self.examination.artifacts["other_manual"], 
                                       self.examination.RR[self.examination.artifacts["other_manual"]],
                                       brush=pg.mkBrush(153, 0, 76, 255), hoverable=True)
        
        """for points in [self.points_T1_auto, self.points_T2_auto, self.points_T3_auto,
                   self.points_T1_manual, self.points_T2_manual, self.points_T3_manual,
                   self.points_diff]:
            points = list(filter(lambda x: x > self.exam_start ))"""

        # oczyszczenie wykresu z poprzednio wyznaczonych artefaktów
        self.p3.clear()
        for el in [self.points_T1_auto, self.points_T2_auto, self.points_T3_auto,
                   self.points_T1_manual, self.points_T2_manual, self.points_T3_manual,
                   self.points_diff]:
            self.p3.addItem(el)

        # ustawienia legendy 
        self.legend.clear()
        self.legend.addItem(self.points_T1_auto, 'auto T1')
        self.legend.addItem(self.points_T2_auto, 'auto T2')
        self.legend.addItem(self.points_T3_auto, 'auto T3')
        self.legend.addItem(self.points_T1_manual, 'manual T1')
        self.legend.addItem(self.points_T2_manual, 'manual T2')
        self.legend.addItem(self.points_T3_manual, 'manual T3')
        self.legend.addItem(self.points_diff, 'other')
        self.legend.setPos(self.legend.mapFromItem(self.legend, QtCore.QPointF(0, max(self.examination.RR))))
