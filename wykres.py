"""
Module in which the plot is defined
"""

import pyqtgraph as pg

def create_graph(obj):
    """
    function to create graph as a widget
    """
    obj.graphWidget = pg.PlotWidget()
    hour = [1,2,3,4,5,6,7,8,9,10]
    temperature = [30,32,34,32,33,31,29,32,35,45]
    obj.graphWidget.setBackground('k')
    obj.graphWidget.plot(hour, temperature)
