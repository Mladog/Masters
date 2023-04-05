"""
Module in which the plot is defined
"""

import pyqtgraph as pg
from PyQt6 import QtCore

def create_graph(obj):
    """
    function to create graph as a widget
    """
    obj.graphWidget = pg.PlotWidget()
    
    obj.graphWidget.setBackground('gray')
    obj.graphWidget.setGeometry(QtCore.QRect(0, 0, 785, 580))
    obj.RR_plot = obj.graphWidget.plot(obj.examination.RR)
    obj.RR_plot.clear()
    obj.label = pg.TextItem(text="X: {} \nY: {}".format(0, 0))
    obj.graphWidget.addItem(obj.label)

    obj.legend = pg.LegendItem()
    obj.legend.setParentItem(obj.RR_plot)
    
    obj.graphWidget.scene().sigMouseMoved.connect(obj.mouse_moved)
    obj.graphWidget.scene().sigMouseClicked.connect(obj.mouse_clicked)

    