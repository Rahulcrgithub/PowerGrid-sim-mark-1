import time
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from output.logger import CSVLogger
from collections import deque
from core.load_profile import LoadProfile
from core.power_calculator import calculate_parameters
from core.models import PowerLine, Load
from core.effects_manager import EffectsManager

# Initialize components
line = PowerLine()
load_profile = LoadProfile(base_kw=50)
load = Load(R=10, L=0.1, C=100e-6)
effects_mgr = EffectsManager()

# Simulation setup
base_voltage = 415
start_time = time.time()
logger = CSVLogger()
fault_times = []
harmonic_times = []

# Data buffers
max_len = 60
time_data = deque(maxlen=max_len)
voltage_data = deque(maxlen=max_len)
current_data = deque(maxlen=max_len)
power_data = deque(maxlen=max_len)
reactive_power_data = deque(maxlen=max_len)
apparent_power_data = deque(maxlen=max_len)
pf_data = deque(maxlen=max_len)
freq_data = deque(maxlen=max_len)
load_kw_data = deque(maxlen=max_len)

# Plot setup
fig, axs = plt.subplots(4, 2, figsize=(12, 8))
axs = axs.ravel()
titles = ["Voltage (V)", "Current (A)", "Active Power (kW)", "Reactive Power (kVAR)",
          "Apparent Power (kVA)", "Power Factor", "Frequency (Hz)", "Load (kW)"]

def update(frame):
    elapsed = int(time.time() - start_time)
    load_kw = load_profile.get_load_kw(elapsed)
    effects = effects_mgr.get_effects(elapsed)

    # Record events
    if effects["harmonics"]:
        harmonic_times.append(elapsed)
    if effects["fault"]:
        fault_times.append(elapsed)

    # Adjust voltage
    V = base_voltage * effects["voltage_offset"] if effects["voltage_offset"] else base_voltage

    # Calculate parameters
    params = calculate_parameters(V, load_kw, load.R, load.L, load.C)
    
    if effects["harmonics"]:
        harmonic = V * effects["harmonics_level"] * math.sin(2 * math.pi * 150 * elapsed)
        params["V"] += harmonic

    params["I"] *= effects["current_multiplier"]

    # Save data
    time_data.append(elapsed)
    voltage_data.append(params["V"])
    current_data.append(params["I"])
    power_data.append(params["P"] / 1000)
    reactive_power_data.append(params["Q"] / 1000)
    apparent_power_data.append(params["S"] / 1000)
    pf_data.append(params["PF"])
    freq_data.append(params["f"])
    load_kw_data.append(load_kw)

    fault_status = ""
    if effects["fault"]:
        fault_type = effects["fault"]
        mag = effects["voltage_offset"] if "voltage_offset" in effects and effects["voltage_offset"] else effects["current_multiplier"]
        fault_status = f"{fault_type} (Mag: {mag:.2f})"

    harmonic_status = ""
    if effects["harmonics"]:
        harmonic_status = f"ON (Level: {effects['harmonics_level']:.3f})"

    logger.log([
        elapsed,
        params["V"],
        params["I"],
        params["P"] / 1000,
        params["Q"] / 1000,
        params["S"] / 1000,
        params["PF"],
        params["f"],
        load_kw,
        fault_status,
        harmonic_status
    ])

    # Update plots
    data_series = [voltage_data, current_data, power_data, reactive_power_data,
                   apparent_power_data, pf_data, freq_data, load_kw_data]
    
    colors = ['tab:red', 'tab:green', 'tab:orange', 'tab:purple', 'tab:cyan', 'tab:brown', 'tab:olive', 'tab:pink']
    y_limits = [(0, 500), (0, 60), (0, 160), (0, 50), (0, 40), (0, 1.1), (49, 51), (0, 100)]

    for i, ax in enumerate(axs):
        ax.clear()
        ax.plot(time_data, data_series[i], color=colors[i])
        ax.set_title(titles[i])
        ax.set_xlabel("Time (s)")
        ax.set_ylim(y_limits[i])
        ax.grid(True)

        # Add vertical markers
    for t in fault_times:
        ax.axvline(x=t, color='red', linestyle='--', alpha=0.3, label='Fault')
    for t in harmonic_times:
        ax.axvline(x=t, color='orange', linestyle='--', alpha=0.2, label='Harmonics')


        # Mark fault and harmonic events
        for t in fault_times:
            if time_data[0] <= t <= time_data[-1]:
                ax.axvline(x=t, color='red', linestyle='--', alpha=0.3)
        for t in harmonic_times:
            if time_data[0] <= t <= time_data[-1]:
                ax.axvline(x=t, color='orange', linestyle='--', alpha=0.2)

ani = animation.FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
plt.tight_layout()
plt.show()
logger.close()
