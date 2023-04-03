"""
Module in which the plot is defined
"""

import pyqtgraph as pg

def create_graph(obj):
    """
    function to create graph as a widget
    """
    graphWidget = pg.PlotWidget()
    graphWidget.setBackground('k')
    graphWidget.plot(obj.examination)

    obj.label = pg.TextItem(text="X: {} \nY: {}".format(0, 0))
    graphWidget.addItem(obj.label)

    graphWidget.scene().sigMouseMoved.connect(obj.mouse_moved)
    graphWidget.scene().sigMouseClicked.connect(obj.mouse_clicked)

    return graphWidget
