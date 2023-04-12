""" 
moduł odpowiedzialny za obsługę wykresu
"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

def create_new_graph(obj):
    """ 
    funkcja tworząca widget zawierający wszystkie elementy wykresów
    """
    # inicjalizacja okna obługującego wykresy
    obj.graphWidget = pg.PlotWidget()
    # tytuł okna
    obj.graphWidget.setWindowTitle('Zarejestrowany sygnal')
    # inicjalizacja pierwszego wykresu z zakresem oraz opisami osi
    obj.p1 = obj.graphWidget.plotItem
    obj.p1.setYRange(-100, 1000, padding=0)
    obj.p1.setXRange(-100, 30000, padding=0)
    obj.p1.setLabels(left='RR [ms]', bottom = 'nr kolejnego interwału')

    # inicjalizacja drugiego wykresu wyświetlajacego artefakty
    obj.p2 = pg.ViewBox()

    # inicjalizacja go wykresu wyświetlajacego ...
    obj.p3 = pg.ViewBox()

    # inicjalizacja wykresu odpowiedzialnego za wyświetlenie aktualnego kliknięcia kursora
    obj.plot_cursor = pg.ViewBox()
    
    # dodanie widoków do wykresu oraz połączenie ich osi
    for p in [obj.p2, obj.p3, obj.plot_cursor]:
        obj.p1.scene().addItem(p)
        p.setXLink(obj.p1)
        p.setYLink(obj.p1)

    # dodanie legendy do wykresu
    obj.legend = pg.LegendItem()
    obj.graphWidget.addItem(obj.legend)
    
    # dodanie etykiety wyświetlającej współrzędne 
    obj.label = pg.TextItem(text="X: {} \nY: {}".format(0, 0))
    obj.graphWidget.addItem(obj.label)
    obj.graphWidget.scene().sigMouseMoved.connect(obj.mouse_moved)
    obj.graphWidget.scene().sigMouseClicked.connect(obj.mouse_clicked)

    # zmiana widoku po aktualizacji wykresu
    def updateViews():
        # dopasowanie wszystkich wykresów do widoku wykresu 1
        for p in [obj.p2, obj.p3, obj.plot_cursor]:
            p.setGeometry(obj.p1.vb.sceneBoundingRect())
            p.linkedViewChanged(obj.p1.vb, p.XAxis)

    updateViews()
    obj.p1.vb.sigResized.connect(updateViews)

def add_point_to_graph(obj):
    obj.plot_cursor.clear()
    obj.cursor_coords = pg.ScatterPlotItem([obj.coords_x], [obj.examination.RR[obj.coords_x]],
                                       brush=pg.mkBrush(0, 255, 0, 120),
                                       size = 12,
                                       hoverable=True)
    obj.plot_cursor.addItem(obj.cursor_coords)