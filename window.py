"""
module containing Window definition
"""

import numpy as np
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from widgets import create_widgets


class Window(QWidget):
    """
    main window of app
    """
    def __init__(self):
        super().__init__()
        self.resize(700, 500)
        self.setWindowTitle("Artefakty")
        self.setWindowIcon(QIcon("icon.jpg"))
        self.fname = ""
        self.examination = []
        self.main_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.art1 = QRadioButton("Typ 1", self)
        self.art2 = QRadioButton("Typ 2", self)
        self.setLayout(self.main_layout)
        create_widgets(self)

    def open_dialog(self):
        """
        file choose
        """
        dialog = QFileDialog()
        dialog.setNameFilter(".csv") #to nie działa
        self.fname, _ = dialog.getOpenFileName(
            self,
            "Open File",
            "examination.xls",
        )
        print(self.fname)
        self.examination = np.genfromtxt(self.fname, delimiter=",")
        self.graphWidget.plot(self.examination)

    def mouse_moved(self, evt):
        vb = self.graphWidget.plotItem.vb
        if self.graphWidget.sceneBoundingRect().contains(evt):
            mouse_point = vb.mapSceneToView(evt)
            self.label.setHtml(f"<p style='color:white'>X： {mouse_point.x()} <br> Y: {mouse_point.y()}</p>")

    def mouse_clicked(self, evt):
        vb = self.graphWidget.plotItem.vb
        scene_coords = evt.scenePos()
        if self.graphWidget.sceneBoundingRect().contains(scene_coords):
            mouse_point = vb.mapSceneToView(scene_coords)
            print(f'clicked plot X: {mouse_point.x()}, Y: {mouse_point.y()}, event: {evt}')

    def btnstate(self, b):
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