import numpy as np
from matplotlib import pyplot as plt

simulation_length = 60
sampling_rate = 10
pid_rate = 10

def L_2_norm(function_values, dt):
    norm = sum(v**2 for v in function_values)*dt
    return norm

log = np.load("logs/6vehicles_0.84tau_dynamicc_0.5headway_10sampling_10pid_vdif.npy")

f, (ax1, ax2) = plt.subplots(1, 2)
colors = plt.cm.get_cmap('hsv', 6)
ax1.plot(np.linspace(0, simulation_length, simulation_length*sampling_rate*pid_rate), log[:, 1, 0], c=colors(0), label="Lead")

for i in range(5):
    ax1.plot(np.linspace(0, simulation_length, simulation_length * sampling_rate * pid_rate), log[:, 1, i+1], c=colors(i + 1),
             label=f"Follower {i+1}")
    # ax1.plot(np.linspace(0, simulation_length, simulation_length * sampling_rate * pid_rate), log[:, 2, i+1], c=colors(i + 1),
             # linestyle="--")
    ax1.plot(np.linspace(0, simulation_length, simulation_length * sampling_rate * pid_rate), log[:, 0, i + 1],
             c=colors(i + 1), linestyle="dotted")
    # ax1.plot(np.linspace(0, simulation_length, simulation_length * sampling_rate * pid_rate), log[:, 3, i + 1],
             # c=colors(i + 1), linestyle="-.")
    ax1.plot(np.linspace(0, simulation_length, simulation_length * sampling_rate * pid_rate), log[:, 4, i + 1],
             c=colors(i + 1), linestyle="--")


vehicle_indices = np.arange(0, 6, 1)
ax2.plot(vehicle_indices, L_2_norm(log[20*pid_rate*sampling_rate:, 2, vehicle_indices], 1.0/(sampling_rate*pid_rate)), label="Acceleration") # start cut off
ax2.plot(vehicle_indices[1:], L_2_norm(log[20*pid_rate*sampling_rate:, 4, vehicle_indices[1:]], 1.0/(sampling_rate*pid_rate)), label="Spacing error")
ax2.set_title(r"$L^2$ norm in vehicle domain")
ax2.legend()
ax1.set_title("Time domain")
ax1.legend()
ax1.set_ylim([-10, 30])
plt.show()