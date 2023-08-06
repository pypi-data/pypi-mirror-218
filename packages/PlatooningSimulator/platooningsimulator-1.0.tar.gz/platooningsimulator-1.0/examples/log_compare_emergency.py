import numpy as np
from matplotlib import pyplot as plt

log_static = np.load("../logs_for_publishing/emergency_3.npy")
# log_dynamic = np.load("../logs_for_publishing/dynamic_cacc_length_100.npy")
log_model = np.load("../logs_for_publishing/emergency_model.npy")
N = log_static.shape[0]
t = np.arange(0, 120, 0.1)
indices = np.linspace(1, N-1, N-1)
colors = plt.cm.get_cmap('Greys_r', N+2)

f, ((ax1, ax3), (ax2, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=True, figsize=(7, 5), dpi=100)

def l_2_norm(y, dt):
	norm_squared = sum(_y**2 for _y in y)*dt
	return np.sqrt(norm_squared)

for j in range(N):
	if j == 0:
		ax1.plot(t[200:], log_static[0, 1, 200:], label="Lead vehicle", c=colors(0), linewidth=1)
		ax2.plot(t[200:], log_model[200:, 1, 0], label="Lead vehicle", c=colors(0), linewidth=1)
		#ax2.plot(t[300:950], log_model[1, 3000:9500:10, 0], label="Lead vehicle", c=colors(0), linewidth=1)
	else:
		ax1.plot(t[200:], log_static[j, 1, 200:], label=f"Follower vehicle {j}", c=colors(j), zorder=-1, linewidth=1)
		ax3.plot(t[200:], log_static[j, 0, 200:], linestyle="dashed", c=colors(j), zorder=-1, linewidth=1)
		#ax4.plot(t[300:950], log_static[j, 0, 300:950]-0.5*log_static[j, 1, 300:950]-5, c=colors(j), linestyle="dotted", linewidth=1)

		ax2.plot(t[200:], log_model[200:, 1, j], label=f"Follower vehicle {j}", c=colors(j), zorder=-1, linewidth=1)
		ax4.plot(t[200:], log_model[200:, 0, j-1] - log_model[200:, 0, j], linestyle="dashed", c=colors(j), zorder=-1, linewidth=1)
		#ax5.plot(t[300:], log_model[j, 0, 300:] - 0.5 * log_model[j, 1, 300:] - 5, c=colors(j), linestyle="dotted",
		#		 linewidth=1)


ax1.set_title(r"Simulation")
ax2.set_title(r"Integrated model")
ax3.set_title(r"Simulation")
ax4.set_title(r"Integrated model")
# ax5.set_title(r"Simulation (dynamic $c$)")
# ax6.set_title(r"Integrated model ($c=2$)")
#
ax1.set_xlabel("Time [s]")
ax2.set_xlabel("Time [s]")
ax3.set_xlabel("Time [s]")
ax4.set_xlabel("Time [s]")
# ax5.set_xlabel("Time [s]")
# ax6.set_xlabel("Time [s]")
#
ax1.set_ylabel("Velocity [m/s]")
ax2.set_ylabel("Velocity [m/s]")
ax3.set_ylabel("Gap [m]")

ax4.set_ylabel("Gap [m]")
# ax5.set_ylabel("Gap, spacing error [m]")
# ax6.set_ylabel("Gap, spacing error [m]")
ax2.legend(bbox_to_anchor=(2.7, 1.5))
plt.show()
