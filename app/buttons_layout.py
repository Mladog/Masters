"""
Moduł służący utworzeniu układu przycisków
"""
from PyQt6.QtWidgets import QPushButton, QButtonGroup

def create_buttons_layout(obj):
    """
    funkcja odpowiedzialna za rozmieszczenie przycisków
    """
    obj.save_btn = QPushButton(obj)
    obj.save_btn.setText("Save")
    obj.save_btn.clicked.connect(lambda:obj.save_data())
    obj.main_layout.addWidget(obj.save_btn)
    
    obj.artifacts_group = QButtonGroup(obj)
    for i, t in enumerate([obj.t1, obj.t2, obj.t3, obj.diff]):
        obj.artifacts_group.addButton(t)
        obj.r_buttons_layout.addWidget(t)

    obj.methods_group = QButtonGroup(obj)
    for i, m in enumerate([obj.m1, obj.m2, obj.m3, obj.m4]):
        obj.methods_group.addButton(m)
        obj.m_buttons_layout.addWidget(m)

    obj.m_buttons_layout.addLayout(obj.pre_mean_buttons_layout)

    obj.pre_mean_buttons_layout.addWidget(obj.m5)
    obj.methods_group.addButton(obj.m5)
    obj.pre_mean_buttons_layout.addWidget(obj.pre_mean_count)

    obj.t1.setChecked(True)
    #obj.toggle_button_selected = "T1"

    obj.m1.setChecked(True)

    for t in [obj.t1_auto, obj.t2_auto, obj.t3_auto,
              obj.t1_man, obj.t2_man, obj.t3_man, obj.diff_man]:
        obj.c_buttons_layout.addWidget(t)

    obj.art_btn = QPushButton(obj)
    obj.art_btn.setText("Mark manually")
    obj.art_btn.clicked.connect(lambda:obj.choose_artifact())
    obj.r_buttons_layout.addWidget(obj.art_btn)       
    
    obj.del_btn = QPushButton(obj)
    obj.del_btn.setText("Delete artifact")
    obj.del_btn.clicked.connect(lambda:obj.del_artifact([obj.coords_x]))
    obj.r_buttons_layout.addWidget(obj.del_btn)    

    obj.del_btn2 = QPushButton(obj)
    obj.del_btn2.setText("Correct chosen")
    obj.del_btn2.clicked.connect(lambda:obj.delete_chosen_artifacts())
    obj.c_buttons_layout.addWidget(obj.del_btn2)

