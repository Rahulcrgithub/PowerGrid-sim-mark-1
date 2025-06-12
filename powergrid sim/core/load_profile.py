import numpy as np

class LoadProfile:
    def __init__(self, base_kw=50):
        self.base_kw = base_kw
        self.prev = base_kw
        self.noise = np.random.normal
        self.t = 0

    def get_load_kw(self, elapsed):
        self.t += 0.01
        variation = np.sin(self.t) * 10 + self.noise(0, 1)  # smoother curve
        load = self.base_kw + variation
        self.prev = load
        return max(0, load)
