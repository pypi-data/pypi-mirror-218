import numpy as np
from matplotlib import pyplot as plt

log_static = np.load("../logs_for_publishing/naive_c_2_length_100_2.npy")
log_dynamic = np.load("../logs_for_publishing/dynamic_cacc_length_100.npy")
log_model = np.load("../logs_for_publishing/cacc_model_c_2_return_20.npy")
N = log_static.shape[0]
t = np.arange(0, 100, 0.1)
indices = np.linspace(1, N-1, N-1)
colors = plt.cm.get_cmap('Greys_r', N+2)

f, ((ax1, ax4), (ax2, ax5), (ax3, ax6)) = plt.subplots(nrows=3, ncols=2, sharex=True, figsize=(7, 5), dpi=100)

def l_2_norm(y, dt):
	norm_squared = sum(_y**2 for _y in y)*dt
	return np.sqrt(norm_squared)

for j in range(N):
	if j == 0:
		ax1.plot(t[300:950], log_static[0, 1, 300:950], label="Lead vehicle", c=colors(0), linewidth=1)
		ax2.plot(t[300:950], log_dynamic[0, 1, 300:950], label="Lead vehicle", c=colors(0), linewidth=1)
		ax3.plot(t[300:950], log_model[1, 3000:9500:10, 0], label="Lead vehicle", c=colors(0), linewidth=1)
	else:
		ax1.plot(t[300:950], log_static[j, 1, 300:950], label=f"Follower vehicle {j}", c=colors(j), zorder=-1, linewidth=1)
		ax4.plot(t[300:950], log_static[j, 0, 300:950], linestyle="dashed", c=colors(j), zorder=-1, linewidth=1)
		ax4.plot(t[300:950], log_static[j, 0, 300:950]-0.5*log_static[j, 1, 300:950]-5, c=colors(j), linestyle="dotted", linewidth=1)

		ax2.plot(t[300:950], log_dynamic[j, 1, 300:950], label=f"Follower vehicle {j}", c=colors(j), zorder=-1, linewidth=1)
		ax5.plot(t[300:950], log_dynamic[j, 0, 300:950], linestyle="dashed", c=colors(j), zorder=-1, linewidth=1)
		ax5.plot(t[300:950], log_dynamic[j, 0, 300:950] - 0.5 * log_dynamic[j, 1, 300:950] - 5, c=colors(j), linestyle="dotted",
				 linewidth=1)

		ax3.plot(t[300:950], log_model[1, 3000:9500:10, j], label=f"Follower vehicle {j}", c=colors(j), zorder=-1, linewidth=1)
		ax6.plot(t[300:950], log_model[0, 3000:9500:10, j], linestyle="dashed", c=colors(j), zorder=-1, linewidth=1)
		ax6.plot(t[300:950], log_model[0, 3000:9500:10, j] - 0.5 * log_model[1, 3000:9500:10, j]-5, c=colors(j), linestyle="dotted",
				 linewidth=1)


ax1.set_title(r"Simulation ($c=2$)")
ax2.set_title(r"Simulation (dynamic $c$)")
ax3.set_title(r"Integrated model ($c=2$)")
ax4.set_title(r"Simulation ($c=2$)")
ax5.set_title(r"Simulation (dynamic $c$)")
ax6.set_title(r"Integrated model ($c=2$)")

ax1.set_xlabel("Time [s]")
ax2.set_xlabel("Time [s]")
ax3.set_xlabel("Time [s]")
ax4.set_xlabel("Time [s]")
ax5.set_xlabel("Time [s]")
ax6.set_xlabel("Time [s]")

ax1.set_ylabel("Velocity [m/s]")
ax2.set_ylabel("Velocity [m/s]")
ax3.set_ylabel("Velocity [m/s]")

ax4.set_ylabel("Gap, spacing error [m]")
ax5.set_ylabel("Gap, spacing error [m]")
ax6.set_ylabel("Gap, spacing error [m]")
ax2.legend(bbox_to_anchor=(2.7, 1.05))
plt.show()


f, (ax7, ax8, ax9) = plt.subplots(nrows=3, sharex=True)
ax7.plot(indices, [l_2_norm(log_static[int(i), 0, 300:950]-5, 0.1) for i in indices], c="black")
ax8.plot(indices, [l_2_norm(log_dynamic[int(i), 0, 300:950]-5, 0.1) for i in indices], c="black")
ax9.plot(indices, [l_2_norm(log_model[0, 3000:9500:10, int(i)]-5, 0.1) for i in indices], c="black")
ax7.set_xlabel("Vehicle index")
ax8.set_xlabel("Vehicle index")
ax9.set_xlabel("Vehicle index")
ax7.set_title(r"Simulation ($c=2$) - $\mathcal{L}_2$-norm of $\Delta_i$")
ax8.set_title(r"Simulation (dynamic $c$) - $\mathcal{L}_2$-norm of $\Delta_i$")
ax9.set_title(r"Integrated model ($c=2$) - $\mathcal{L}_2$-norm of $\Delta_i$")
plt.show()