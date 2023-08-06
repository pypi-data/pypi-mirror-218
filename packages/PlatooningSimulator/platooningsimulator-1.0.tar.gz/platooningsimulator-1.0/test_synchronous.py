import carla
from src.PlatooningSimulator import Core, PlatooningControllers
import numpy as np
from matplotlib import pyplot as plt

tau = 0.84
h = 0.5  # time headway
c = "dynamic"  # controller constant


def vehicle_model(t, y, u):
    return np.array([y[1], 1/tau * (-y[1]+u)])


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


def v_ref_cruise(predecessor, ego):
    length = 5  # vehicle length
    d = ego.distance_to(predecessor)  # distance between cars
    speed_i_1 = predecessor.speed  # speed in m/s
    speed_i = ego.speed
    return (tau / h * (speed_i_1 - speed_i + c * (d - length - h * speed_i)) + speed_i) * 3.6


def v_ref_cruise_dynamic(predecessor, ego):
    length = 5
    a_max = 3
    c_standard = 2
    c_min = 0.5
    d = ego.distance_to(predecessor)
    speed_i_1 = predecessor.speed
    speed_i = ego.speed
    dynamic_c = max(c_min, min(c_standard, 1/(d - length - h * speed_i) * (h*a_max - speed_i_1 + speed_i)))
    return (tau / h * (speed_i_1 - speed_i + dynamic_c * (d - length - h * speed_i)) + speed_i) * 3.6


def L_2_norm(function_values, dt):
    norm = sum(v**2 for v in function_values)*dt
    return norm


simulation_length = 60
sampling_rate = 10
pid_rate = 10

s = Core.Simulation(render=True, world="Town11", synchronous=True, dt=round(1.0 / (sampling_rate * pid_rate), 3))

vehicle_blueprints = s.world.get_blueprint_library().filter('*vehicle*')
bp = vehicle_blueprints[4]
bp.set_attribute('role_name', 'hero')
spawn_points = s.map.get_spawn_points()

platoon = Core.Platoon(s)
lead_vehicle = platoon.add_lead_vehicle(bp, point_straight_ahead(spawn_points[20], 40))
s.world.tick()      # important for leadNavi to get actual starting position
leadNavi = PlatooningControllers.LeadNavigator(lead_vehicle)
lead_vehicle.attach_controller(leadNavi)
followers = []
# linearParams = [(-1, "get_location"), (0, "get_location"), (-1, "get_velocity"), (0, "get_velocity")]
deps = [-1, 0]
for i in range(0, 6):
    v = platoon.add_follower_vehicle(bp, point_straight_ahead(spawn_points[20], -10*(i-3)), history_depth=10, history_data=["speed"])
    linearController = PlatooningControllers.FollowerController(v, v_ref_cruise_dynamic, platoon, dependencies=deps)
    v.attach_controller(linearController)
    followers.append(v)

log = np.zeros([simulation_length*sampling_rate*pid_rate, 5, len(followers)+1])

# s.add_platoon(platoon)
leadNavi.set_target_speed(25*3.6)
s.world.tick()
for i in range(0, pid_rate*sampling_rate*simulation_length):
    # tic = time.time()
    initial_location = lead_vehicle.get_transform().location
    s.run_step(mode="sample" if i % sampling_rate == 0 else "control")
    if i == 15*sampling_rate*pid_rate:
        second_platoon, second_leadNavi = platoon.split(3, 6)
        leadNavi.set_target_speed(26*3.6)
        # second_leadNavi.set_target_speed(20*3.6)

    if i == 20*sampling_rate*pid_rate:
        platoon.merge(second_platoon)

    log[i, 1, 0] = lead_vehicle.speed
    log[i, 2, 0] = lead_vehicle.acceleration
    log[i, 3, 0] = leadNavi.target_speed / 3.6
    for j, fv in enumerate(followers):
        log[i, 0, j+1] = fv.distance_to(followers[j-1] if j > 0 else lead_vehicle)
        log[i, 1, j+1] = fv.speed
        log[i, 2, j+1] = (fv.speed - (log[i-1, 1, j+1] if i > 0 else 0))*pid_rate*sampling_rate  # fv.acceleration
        log[i, 3, j+1] = fv.controller.target_speed / 3.6
        log[i, 4, j+1] = fv.distance_to(followers[j-1] if j > 0 else lead_vehicle) - 5 - h*fv.speed
    if i % 100 == 0:
        s_transform = followers[-1].get_transform()
        s_transform.location.z += 5
        s.spectator.set_transform(point_straight_ahead(s_transform, -10))
    s.world.tick()
    # try:
    #     time.sleep(1.0/(sampling_rate*pid_rate)-(time.time()-tic))
    # except ValueError:
    #     print("out of synch")

f, (ax1, ax2) = plt.subplots(1, 2)
colors = plt.cm.get_cmap('hsv', len(followers) + 1)
ax1.plot(np.linspace(0, simulation_length, simulation_length*sampling_rate*pid_rate), log[:, 1, 0], c=colors(0), label="Lead")
# ax1.plot(np.linspace(0, simulation_length, simulation_length*sampling_rate*pid_rate), log[:, 2, 0], c=colors(0), linestyle="--")

for i, fv in enumerate(followers):
    ax1.plot(np.linspace(0, simulation_length, simulation_length * sampling_rate * pid_rate), log[:, 1, i+1], c=colors(i + 1),
             label=f"Follower {i+1}")
    # ax1.plot(np.linspace(0, simulation_length, simulation_length * sampling_rate * pid_rate), log[:, 2, i+1], c=colors(i + 1),
             # linestyle="--")
    ax1.plot(np.linspace(0, simulation_length, simulation_length * sampling_rate * pid_rate), log[:, 0, i + 1],
             c=colors(i + 1), linestyle="dotted")
    ax1.plot(np.linspace(0, simulation_length, simulation_length * sampling_rate * pid_rate), log[:, 3, i + 1],
             c=colors(i + 1), linestyle="-.")
    ax1.plot(np.linspace(0, simulation_length, simulation_length * sampling_rate * pid_rate), log[:, 4, i + 1],
             c=colors(i + 1), linestyle="--")

np.save(f"logs/{len(followers)}vehicles_{tau}tau_{c}c_{h}headway_{sampling_rate}sampling_{pid_rate}pid_vdif.npy", log)

print(followers[0].history.speed)

vehicle_indices = np.arange(0, len(followers)+1, 1)
ax2.plot(vehicle_indices, L_2_norm(log[1*pid_rate*sampling_rate:, 2, vehicle_indices], 1.0/(sampling_rate*pid_rate)), label="Acceleration") # start cut off
ax2.plot(vehicle_indices[1:], L_2_norm(log[1*pid_rate*sampling_rate:, 4, vehicle_indices[1:]], 1.0/(sampling_rate*pid_rate)), label="Spacing error")
ax2.set_title(r"$L^2$ norm in vehicle domain")
ax2.legend()
ax1.set_title("Time domain")
ax1.legend()
ax1.set_ylim([-10, 30])
plt.show()