"""
module to create functions buttons 
"""
from PyQt6.QtWidgets import QPushButton

def create_blayout(obj):
    """
    function responsible for creating the layout
    """
    back_btn = QPushButton(obj)
    back_btn.setText("Cofnij")
    obj.main_layout.addWidget(back_btn)

    for type_x in [obj.t1, obj.t2, obj.t3, obj.t4, obj.t5, obj.t6]:
        type_x.setChecked(True)
        type_x.toggled.connect(lambda:obj.btnstate(type_x))
        obj.buttons_layout.addWidget(type_x)

    art_btn = QPushButton(obj)
    art_btn.setText("Oznacz artefakt")
    obj.buttons_layout.addWidget(art_btn)
    