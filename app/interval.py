

class Interval():
    def __init__(self, value):
        self.value = float(value)
        self.artifact_type = None
        self.correction_methods = {
            "linear interpolation": 0,
            "cubic splain": 0,
            "deletion": 0,
            "moving average": 0,
            "Marcel": 0
        }
