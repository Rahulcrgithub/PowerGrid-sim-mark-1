class PowerLine:
    def __init__(self, voltage=415.0, frequency=50.0):
        self.voltage = voltage
        self.frequency = frequency

class Load:
    def __init__(self, R, L, C):
        self.R = R
        self.L = L
        self.C = C
