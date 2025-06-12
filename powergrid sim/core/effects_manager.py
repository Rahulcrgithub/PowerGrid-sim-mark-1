import random
import time

class EffectsManager:
    def __init__(self):
        self.last_harmonic_trigger = 0
        self.harmonic_duration = 300  # Harmonics last for 5 minutes
        self.harmonic_next_trigger = random.randint(300, 600)

        self.last_fault_trigger = 0
        self.fault_duration = 10  # Fault lasts for 10 seconds
        self.fault_next_trigger = random.randint(900, 1500)

        self.active_fault = None
        self.active_harmonics = False
        self.harmonics_level = 0
        self.fault_magnitude = 0

    def get_effects(self, elapsed_sec):
        effects = {
            "harmonics": False,
            "harmonics_level": 0,
            "fault": None,
            "fault_magnitude": 0,
            "voltage_offset": 1.0,
            "current_multiplier": 1.0
        }

        # === Harmonic effect logic ===
        if not self.active_harmonics and (elapsed_sec - self.last_harmonic_trigger) > self.harmonic_next_trigger:
            self.active_harmonics = True
            self.last_harmonic_trigger = elapsed_sec
            self.harmonic_next_trigger = random.randint(300, 600)  # Schedule next harmonic
            self.harmonics_level = random.uniform(0.01, 0.05)

        if self.active_harmonics:
            effects["harmonics"] = True
            effects["harmonics_level"] = self.harmonics_level

            # Stop harmonics after duration
            if (elapsed_sec - self.last_harmonic_trigger) > self.harmonic_duration:
                self.active_harmonics = False
                self.harmonics_level = 0

        # === Fault effect logic ===
        if not self.active_fault and (elapsed_sec - self.last_fault_trigger) > self.fault_next_trigger:
            self.last_fault_trigger = elapsed_sec
            self.fault_next_trigger = random.randint(900, 1500)
            self.active_fault = random.choice(["overvoltage", "undervoltage", "overcurrent", "sag", "swell"])

            # Set magnitude
            if self.active_fault == "overvoltage":
                self.fault_magnitude = random.uniform(1.2, 1.4)
            elif self.active_fault == "undervoltage":
                self.fault_magnitude = random.uniform(0.6, 0.8)
            elif self.active_fault == "overcurrent":
                self.fault_magnitude = random.uniform(1.3, 1.5)
            elif self.active_fault == "sag":
                self.fault_magnitude = random.uniform(0.7, 0.9)
            elif self.active_fault == "swell":
                self.fault_magnitude = random.uniform(1.1, 1.3)

        if self.active_fault:
            effects["fault"] = self.active_fault

            if self.active_fault in ["overvoltage", "undervoltage", "sag", "swell"]:
                effects["voltage_offset"] = self.fault_magnitude
            elif self.active_fault == "overcurrent":
                effects["current_multiplier"] = self.fault_magnitude

            # Clear fault after duration
            if (elapsed_sec - self.last_fault_trigger) > self.fault_duration:
                self.active_fault = None
                self.fault_magnitude = 0

        return effects
