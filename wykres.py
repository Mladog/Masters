"""
Module in which the plot is defined
"""

import pyqtgraph as pg

def create_graph(obj):
    """
    function to create graph as a widget
    """
    obj.graphWidget = pg.PlotWidget()
    obj.graphWidget.setBackground('k')
    obj.graphWidget.plot(obj.examination)

    obj.label = pg.TextItem(text="X: {} \nY: {}".format(0, 0))
    obj.graphWidget.addItem(obj.label)


    obj.graphWidget.scene().sigMouseMoved.connect(obj.mouse_moved)
    obj.graphWidget.scene().sigMouseClicked.connect(obj.mouse_clicked)
