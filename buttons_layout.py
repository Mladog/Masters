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

    for t in [obj.t1, obj.t2, obj.t3]:
        #t.toggled.connect(lambda:obj.btnstate(t))
        obj.r_buttons_layout.addWidget(t)

    obj.t1.setChecked(True)
    obj.toggle_button_selected = "T1"

    for t in [obj.t1_auto, obj.t2_auto, obj.t3_auto,
              obj.t1_man, obj.t2_man, obj.t3_man, obj.current]:
        obj.c_buttons_layout.addWidget(t)

    obj.art_btn = QPushButton(obj)
    obj.art_btn.setText("Oznacz artefakt")
    obj.art_btn.clicked.connect(lambda:obj.choose_artifact())
    obj.r_buttons_layout.addWidget(obj.art_btn)       
    
    obj.del_btn = QPushButton(obj)
    obj.del_btn.setText("Usuń artefakt")
    obj.del_btn.clicked.connect(lambda:obj.del_artifact())
    obj.r_buttons_layout.addWidget(obj.del_btn)    