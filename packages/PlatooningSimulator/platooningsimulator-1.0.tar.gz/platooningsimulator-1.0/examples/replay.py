import carla
from matplotlib import pyplot as plt
import numpy as np

client = carla.Client("localhost", 2000)
# print(client.show_recorder_file_info("C:/Dev/Carla_logs/recording_1_test.log", show_all=True))
client.replay_file("C:/Dev/Carla_logs/emergency_recording_3.log", 0, 0, 126)

log = np.load("../logs_for_publishing/emergency_3.npy")
N = log.shape[0]
colors = plt.cm.get_cmap('RdYlBu', N)
t = np.arange(0, 120, 0.1)

plt.figure(figsize=(10, 7), dpi=150)

for j in range(N):
	if j == 0:
		plt.plot(t[1:], log[0, 1, 1:], label="Lead vehicle", c=colors(0))
	else:
		plt.plot(t[1:], log[j, 1, 1:], label=f"Follower vehicle {j}", c=colors(j), zorder=-1)
		plt.plot(t[1:], log[j, 0, 1:], linestyle="dashed", c=colors(j), zorder=-1)
		plt.plot(t[1:], log[j, 0, 1:]-0.5*log[j, 1, 1:]-5, c=colors(j), linestyle="dotted")

plt.plot([20, 20], [0, 0], label="Velocity", c="black", linestyle="solid")
plt.plot([20, 20], [0, 0], label="Gap", c="black", linestyle="dashed")
plt.plot([20, 20], [0, 0], label="Spacing error", c="black", linestyle="dotted")


plt.legend()
plt.show()
