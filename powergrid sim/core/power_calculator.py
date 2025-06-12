import math
import random

def calculate_parameters(V, load_kw, R, L , C, freq=50):
    XL = 2 * math.pi * freq * L
    XC = 1 / (2 * math.pi * freq * C) if C != 0 else 0
    Z = math.sqrt(R**2 + (XL - XC)**2)

    base_I = V / Z
    # Add small dynamic fluctuations (±3%)
    I = base_I * random.uniform(0.97, 1.03)

    P = load_kw * 1000
    S = V * I

    s2_p2 = S**2 - P**2
    Q = math.sqrt(s2_p2) if s2_p2 > 0 else 0
    PF = P / S if S != 0 else 0
    return {
        "I": I,
        "P": P,
        "Q": Q,
        "S": S,
        "PF": PF,
        "Z": Z,
        "V": V,
        "f": freq
    }
