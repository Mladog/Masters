"""
Modul odpowiedzialny za obsługę klasy Examination 
"""

class Examination():
    """
    Klasy Examination, pozwalajaca na wydobycie podstawowych informacji o badaniu
    """
    def __init__(self, exam_id, exam_fs = 250, source = "COMS"):
        self.path = LOCAL_EXAMINATION_DIRECTORY
        self.source = source
        self.exam_id = exam_id
        self.exam_fs = exam_fs