from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

def create_graph(object):
        object.graphWidget = pg.PlotWidget()
        
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        object.graphWidget.setBackground('k')
        object.graphWidget.plot(hour, temperature)