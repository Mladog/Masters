"""
module to create functions buttons 
"""
from PyQt6.QtWidgets import *

def create_blayout(obj):
    """
    function responsible for creating the layout
    """
    obj.buttons_layout.addWidget(obj.graphWidget)
    back_btn = QPushButton(obj)
    back_btn.setText("Cofnij")
    obj.buttons_layout.addWidget(back_btn)
    back_btn = QPushButton(obj)
    back_btn.setText("Oznacz artefakt")
    obj.buttons_layout.addWidget(back_btn)

    obj.art1.setChecked(True)
    obj.art1.toggled.connect(lambda:obj.btnstate(obj.art1))
    obj.buttons_layout.addWidget(obj.art1)
		
    obj.art2.setChecked(True)
    obj.art2.toggled.connect(lambda:obj.btnstate(obj.art2))
    obj.buttons_layout.addWidget(obj.art2)
		
    