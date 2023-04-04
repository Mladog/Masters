"""
Moduł służący utworzeniu układu przycisków
"""
from PyQt6.QtWidgets import QPushButton

def create_buttons_layout(obj):
    """
    funkcja odpowiedzialna za rozmieszczenie przycisków
    """
    obj.back_btn = QPushButton(obj)
    obj.back_btn.setText("Cofnij")
    obj.main_layout.addWidget(obj.back_btn)

    for t in [obj.t1, obj.t2, obj.t3, obj.t4, obj.t5, obj.t6]:
        #t.setChecked(False)
        t.toggled.connect(lambda:obj.btnstate(t))
        obj.buttons_layout.addWidget(t)

    obj.t1.setChecked(True)
    obj.toggle_button_selected = "T1"

    obj.art_btn = QPushButton(obj)
    obj.art_btn.setText("Oznacz artefakt")
    obj.art_btn.clicked.connect(lambda:obj.check_artifact())
    obj.buttons_layout.addWidget(obj.art_btn)


                
    