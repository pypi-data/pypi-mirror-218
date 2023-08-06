from src.PlatooningSimulator import Core, PlatooningControllers
import numpy as np
from matplotlib import pyplot as plt

tau = 0.66
h = 0.5  # time headway
c = 2

# os.system("C:\Dev\Carla_0.9.14\WindowsNoEditor\CarlaUE4 --quality-level=Low")
def v_ref_cruise(predecessor, ego):
    length = 5  # vehicle length
    d = ego.distance_to(predecessor)  # distance between cars
    speed_i_1 = predecessor.speed  # speed in m/s
    speed_i = ego.speed
    return (tau / h * (speed_i_1 - speed_i + c * (d - length - h * speed_i)) + speed_i) * 3.6


simulation_length = 120
sampling_rate = 10
pid_rate = 10
N = 4
log = np.zeros([N, 3, simulation_length*sampling_rate])
t = np.linspace(0, simulation_length*sampling_rate-1, simulation_length*sampling_rate)

simulation = Core.Simulation(world="Town06", dt=float(1 / sampling_rate / pid_rate), large_map=False, render=True)

bps = simulation.get_vehicle_blueprints()
for b in bps:
    print(b)
    if b.id == "vehicle.bmw.grandtourer":
        bp = b

spawn_points = simulation.map.get_spawn_points()

platoon = Core.Platoon(simulation)
lead_vehicle = platoon.add_lead_vehicle(bp, spawn_points[25])
simulation.tick()      # important for leadNavi to get actual starting position


tm = simulation.get_trafficmanager()
tm.set_synchronous_mode(True)
tm_port = tm.get_port()
lead_vehicle.set_autopilot(True, tm_port)
tm.ignore_lights_percentage(lead_vehicle._carla_vehicle, 100) # ignoring red lights

colors = plt.cm.get_cmap('turbo', N)
followers = []

deps = [-1, 0]

for i in range(0, N-1):
    v = platoon.add_follower_vehicle(bp, (lead_vehicle.transform_ahead(-10, force_straight=True) if i == 0
                                          else followers[i-1].transform_ahead(-10, force_straight=True)))
    linearController = PlatooningControllers.FollowerController(v, v_ref_cruise, platoon, dependencies=deps)
    v.attach_controller(linearController)
    followers.append(v)
    simulation.tick()

# simulation.start_recorder("C:/Dev/Carla_logs/autopilot_recording_2.log", True)

for i in range(simulation_length*pid_rate*sampling_rate):
    simulation.run_step(mode="sample" if i % pid_rate == 0 else "control")

    if i % 100 == 0:
        s_transform = platoon[0].transform_ahead(30, force_straight=True)
        s_transform.location.z += 8
        s_transform.rotation.yaw += 180
        simulation.spectator.set_transform(s_transform)

    if i % pid_rate:
        for j, vehicle in enumerate(platoon):
            log[j, 1, int(i/pid_rate)] = vehicle.speed
            if i > 0:
                log[j, 2, int(i/pid_rate)] = (vehicle.speed - log[j, 1, int(i/pid_rate)-1]) / sampling_rate
            if j > 0:
                log[j, 0, int(i/pid_rate)] = vehicle.distance_to(platoon[j-1])
    simulation.tick()

# simulation.release_synchronous()
# simulation.stop_recorder()

# np.save("C:/Users/Áron Karakai/Documents/RUG/String Stability Research/Platooning_Simulator/logs_for_publishing/autopilot_2.npy", log)


for j, vehicle in enumerate(platoon):
    plt.plot(t, log[j, 1, :], label=f"vehicle {j}", c=colors(j))
    if j > 0:
        plt.plot(t[1:], log[j, 0, 1:], linestyle="dashed", c=colors(j))

plt.legend()
plt.show()
