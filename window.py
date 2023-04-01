"""
module containing Window definition
"""

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileDialog, QVBoxLayout, QWidget

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
        layout = QVBoxLayout()
        self.setLayout(layout)
        create_widgets(self, layout)

    def open_dialog(self):
        """
        file choose
        """
        dialog = QFileDialog()
        dialog.setNameFilter(".xlsx") #to nie działa
        self.fname = dialog.getOpenFileName(
            self,
            "Open File",
            "examination.xls",
        )
        print(self.fname)
