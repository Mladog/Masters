import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

def create_new_graph(obj):
    obj.graphWidget = pg.PlotWidget()
    obj.graphWidget.setWindowTitle('Zarejestrowany sygnal')
    obj.p1 = obj.graphWidget.plotItem
    obj.p1.setYRange(-100, 1000, padding=0)
    obj.p1.setXRange(-100, 30000, padding=0)
    obj.p1.setLabels(left='RR [ms]', bottom = 'czas [ms]')

    ## create a new ViewBox, link the right axis to its coordinate system
    obj.p2 = pg.ViewBox()
    obj.p1.scene().addItem(obj.p2)
    obj.p2.setXLink(obj.p1)
    obj.p2.setYLink(obj.p1)

    ## create third ViewBox. 
    ## this time we need to create a new axis as well.
    obj.p3 = pg.ViewBox()
    obj.p1.scene().addItem(obj.p3)
    obj.p3.setXLink(obj.p1)
    obj.p3.setYLink(obj.p1)

    obj.legend = pg.LegendItem()
    obj.legend.setParentItem(obj.p1)
    
    ## label with information about mouse location
    obj.label = pg.TextItem(text="X: {} \nY: {}".format(0, 0))
    obj.graphWidget.addItem(obj.label)
    obj.graphWidget.scene().sigMouseMoved.connect(obj.mouse_moved)
    obj.graphWidget.scene().sigMouseClicked.connect(obj.mouse_clicked)

    ## Handle view resizing 
    def updateViews():
        ## view has resized; update auxiliary views to match
        obj.p2.setGeometry(obj.p1.vb.sceneBoundingRect())
        #obj.p3.setGeometry(obj.p1.vb.sceneBoundingRect())
        
        ## need to re-update linked axes since this was called
        ## incorrectly while views had different shapes.
        ## (probably this should be handled in ViewBox.resizeEvent)
        obj.p2.linkedViewChanged(obj.p1.vb, obj.p2.XAxis)
        #obj.p3.linkedViewChanged(obj.p1.vb, obj.p3.XAxis)

    updateViews()
    obj.p1.vb.sigResized.connect(updateViews)
    #obj.p2_plot = pg.PlotCurveItem([0, 1]*100, pen='b')
    #obj.p2.addItem(obj.p2_plot)

