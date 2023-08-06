import numpy as np
from matplotlib import pyplot as plt

log = np.load("logs_for_publishing/autopilot_2.npy")

t = np.arange(0, 120, 0.1)

N = log.shape[0]
colors = plt.cm.get_cmap('Greys_r', N+3)

def l_2_norm(y, dt):
	norm_squared = sum(_y**2 for _y in y)*dt
	return np.sqrt(norm_squared)

plt.figure(figsize=(10, 7), dpi=150)
for j in range(N):
	if j == 0:
		plt.plot(t[100:], log[0, 1, 100:], label="Lead vehicle", c=colors(0), linewidth=1)
	else:
		plt.plot(t[100:], log[j, 1, 100:], label=f"Follower vehicle {j}", c=colors(j), zorder=-1, linewidth=1)
		plt.plot(t[100:], log[j, 0, 100:], linestyle="dashed", c=colors(j), zorder=-1, linewidth=1)
		plt.plot(t[100:], log[j, 0, 100:]-0.5*log[j, 1, 100:]-5, c=colors(j), linestyle="dotted", linewidth=1)

# plt.plot([20, 20], [0, 0], label="Velocity", c="black", linestyle="solid")
# plt.plot([20, 20], [0, 0], label="Gap", c="black", linestyle="dashed")
# plt.plot([20, 20], [0, 0], label="Spacing error", c="black", linestyle="dotted")


plt.xlabel("Time [s]")
plt.ylabel("Velocity [m/s], gap [m], spacing error [m]")
# plt.legend(labels=["Lead vehicle"]+[f"Follower vehicle{j}" for j in range(1,N)], ncols=2, loc="center right") #, bbox_to_anchor = (1.505, 0.5)
# plt.legend(labels=["Velocity", "Gap", "Spacing error"])
# plt.legend(loc="upper right", bbox_to_anchor=(1.25, 1))
plt.legend(loc="lower right")

# plt.title(r"Emergency braking")
plt.show()

plt.figure(figsize=(5, 7), dpi=150)

plt.title(r"$\mathcal{L}_2$-norm of $\Delta_i$")
plt.plot([i for i in range(1, N)], [l_2_norm((log[j, 0, :]-5*np.ones(1200)), 0.1) for j in range(1, N)], c="black")  # -5*np.ones(100*10)
plt.xlabel("Vehicle index")
#plt.show()