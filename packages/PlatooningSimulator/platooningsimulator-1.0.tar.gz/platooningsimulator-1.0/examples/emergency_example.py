from src.PlatooningSimulator import Core, PlatooningControllers
import numpy as np
from matplotlib import pyplot as plt
import carla

tau = 0.66
h = 0.5  # time headway
c = 2

lambda1 = -1
lambda2 = -2
emergency_k = lambda1*lambda2
emergency_c = -lambda1-lambda2
k = 0.5
emergency_distance = 5


def point_straight_ahead(initial_transform, distance):
	x = initial_transform.location.x
	y = initial_transform.location.y
	z = initial_transform.location.z
	pitch = np.deg2rad(initial_transform.rotation.pitch)
	yaw = np.deg2rad(initial_transform.rotation.yaw)

	x = x + np.cos(yaw)*np.cos(pitch)*distance
	y = y + np.sin(yaw)*np.cos(pitch)*distance
	z = z + np.sin(pitch)*distance

	return carla.Transform(carla.Location(x=x, y=y, z=z), initial_transform.rotation)

def emergency_controller(predecessor, ego):
	if ego.speed < 0.1 and np.abs(ego.distance_to(predecessor)-emergency_distance) < 0.1:
		return 0
	d = ego.distance_to(predecessor)-emergency_distance
	d_dot = predecessor.speed - ego.speed
	u = tau * (emergency_k * d + emergency_c * d_dot) - d_dot
	return u


def v_ref_cruise(predecessor, ego):
	length = 5  # vehicle length
	d = ego.distance_to(predecessor)  # distance between cars
	speed_i_1 = predecessor.speed  # speed in m/s
	speed_i = ego.speed
	return (tau / h * (speed_i_1 - speed_i + c * (d - length - h * speed_i)) + speed_i) * 3.6


simulation_length = 120
sampling_rate = 10
pid_rate = 10
N = 8
log = np.zeros([N, 3, simulation_length*sampling_rate])

simulation = Core.Simulation(world="Town11", dt=float(1 / sampling_rate / pid_rate), large_map=True, render=False)

bps = simulation.get_vehicle_blueprints()
for b in bps:
	print(b)
	if b.id == "vehicle.bmw.grandtourer":
		bp = b

spawn_points = simulation.map.get_spawn_points()

platoon = Core.Platoon(simulation)
lead_vehicle = platoon.add_lead_vehicle(bp, point_straight_ahead(spawn_points[20], 40))
simulation.world.tick()      # important for leadNavi to get actual starting position

lead_navi = PlatooningControllers.LeadNavigator(lead_vehicle)
lead_vehicle.attach_controller(lead_navi)

followers = []

deps = [-1, 0]

for i in range(0, N-1):
	v = platoon.add_follower_vehicle(bp, point_straight_ahead(spawn_points[20], -10*(i-3)))
	linearController = PlatooningControllers.FollowerController(v, v_ref_cruise, platoon, dependencies=deps, handbrake_on_stop=True)
	v.attach_controller(linearController)
	followers.append(v)

lead_navi.set_target_speed(25*3.6)
simulation.world.tick()

simulation.start_recorder("C:/Dev/Carla_logs/emergency_recording_3.log")

for i in range(simulation_length*pid_rate*sampling_rate):
	simulation.run_step(mode="sample" if i % pid_rate == 0 else "control")

	if i == 30*sampling_rate*pid_rate:
		lead_navi.set_target_speed(0)
		for j, vehicle in enumerate(platoon):
			if j > 0:
				vehicle.controller.control_function = emergency_controller

	if i % 100 == 0:
		s_transform = platoon[0].get_transform()
		s_transform.location.z += 8
		s_transform.rotation.yaw += 180
		simulation.spectator.set_transform(point_straight_ahead(s_transform, -30))

	if i % pid_rate:
		for j, vehicle in enumerate(platoon):
			log[j, 1, int(i/pid_rate)] = vehicle.speed
			if i > 0:
				log[j, 2, int(i/pid_rate)] = (vehicle.speed - log[j, 1, int(i/pid_rate)-1]) / sampling_rate
			if j > 0:
				log[j, 0, int(i/pid_rate)] = vehicle.distance_to(platoon[j-1])
	simulation.world.tick()

np.save(f"../logs_for_publishing/emergency_3.npy", log)
colors = plt.cm.get_cmap('turbo', N)
t = np.linspace(0, simulation_length, simulation_length*sampling_rate)
for j, vehicle in enumerate(platoon):
	plt.plot(t, log[j, 1, :], label=f"vehicle {j}", c=colors(j))
	if j > 0:
		plt.plot(t[1:], log[j, 0, 1:], linestyle="dashed", c=colors(j))

plt.legend()
plt.show()



