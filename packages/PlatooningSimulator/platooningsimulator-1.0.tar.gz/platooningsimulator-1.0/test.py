import carla
from src.PlatooningSimulator import Core, PlatooningControllers
from agents.navigation import local_planner
import numpy as np
import time
from matplotlib import pyplot as plt


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


s = Core.Simulation(render=True, world="Town11")

vehicle_blueprints = s.world.get_blueprint_library().filter('*vehicle*')
print(vehicle_blueprints)
spawn_points = s.map.get_spawn_points()
s.map.generate_waypoints(0.5)


def u(v):
    # print(v)
    velocity = lv.get_velocity()
    return np.sqrt(velocity.x**2 + velocity.y**2 + velocity.y**2)*3.6


def v_ref(s_i_1, s_i, v_i_1, v_i):
    length = 5  # vehicle length
    tau = 0.84
    h = 0.5  # time headway
    c = 1  # controller constant
    d = s_i_1().distance(s_i())  # distance between cars
    _v_i_1 = v_i_1()
    _v_i = v_i()
    speed_i_1 = np.sqrt(_v_i_1.x**2 + _v_i_1.y**2 + _v_i_1.z**2)  # speed in m/s
    speed_i = np.sqrt(_v_i.x ** 2 + _v_i.y ** 2 + _v_i.z ** 2)
    return (tau / h * (speed_i_1 - speed_i + c * (d - length - h * speed_i)) + speed_i) * 3.6


def emergency_v_ref(s_i_1, s_i, v_i_1, v_i):
    tau = 0.84
    c = 0.5  # controller constants
    k = 1.5
    emergency_distance = 5
    d = s_i_1().distance(s_i())-emergency_distance  # distance between cars
    _v_i_1 = v_i_1()
    _v_i = v_i()
    speed_i_1 = np.sqrt(_v_i_1.x ** 2 + _v_i_1.y ** 2 + _v_i_1.z ** 2)  # speed in m/s
    speed_i = np.sqrt(_v_i.x ** 2 + _v_i.y ** 2 + _v_i.z ** 2)
    d_dot = speed_i_1-speed_i
    return (tau*(c*d+k*d_dot)-d_dot) * 3.6


def zero(*args):
    return 0


p = Core.Platoon(s)
bp = vehicle_blueprints[4]
bp.set_attribute('role_name', 'hero')
lv = p.add_lead_vehicle(bp, point_straight_ahead(spawn_points[20], 0))  #s.map.get_waypoint(spawn_points[6].location).next(10.0)[1].transform)
localPlanner = local_planner.LocalPlanner(lv,
                                 {"longitudinal_control_dict": {'K_P': 2/5, 'K_I': 0.26/2, 'K_D': 0.26/3, 'dt': 0.01}})
leadNavi = PlatooningControllers.LeadNavigator(lv)
lv.attach_controller(leadNavi)
followers = []
linearParams = [(-1, "get_location"), (0, "get_location"), (-1, "get_velocity"), (0, "get_velocity")]
for i in range(0, 4):
    v = p.add_follower_vehicle(bp, point_straight_ahead(spawn_points[20], -10*(i+1)))
    linearController = PlatooningControllers.FollowerController(v, v_ref, linearParams, p)
    v.attach_controller(linearController)
    followers.append(v)
# params = [(-1, "get_velocity")]
# fcontrol = Core.FollowerController(fv, u, params, p)



vehicle_waypoint = s.map.get_waypoint(lv.get_location())
print(lv.get_transform())
print(vehicle_waypoint)
# print(vehicle_waypoint.next(10.0))

s.spectator.set_transform(lv.get_transform())

log_lead = np.zeros(7000)
log_followers = np.zeros([7000, len(followers)])

distance_logs = np.zeros([7000, len(followers)])

trajectories = np.zeros([14000, len(followers)+1])

s.add_platoon(p)
leadNavi.set_target_speed(25*3.6)
localPlanner.set_speed(25*3.6)
time.sleep(2)
for i in range(0, 7000):
    # s.world.wait_for_tick()
    tic = time.time()
    s.run_step(mode="sample" if i % 10 == 0 else "control")
    if i == 2800:
        leadNavi.set_target_speed(26*3.6)

    elif i == 5000:
        leadNavi.set_target_speed(0)
        for f in followers:
            f.controller.control_function = emergency_v_ref
            f.controller.handbrake_on_stop = True
    v_1 = lv.get_velocity()
    log_lead[i] = np.sqrt(v_1.x ** 2 + v_1.y ** 2 + v_1.z ** 2)
    pos_l = lv.get_location()
    trajectories[2 * i, 0], trajectories[2 * i + 1, 0] = pos_l.x, pos_l.y
    for j, fv in enumerate(followers):
        v_2 = fv.get_velocity()
        log_followers[i, j] = np.sqrt(v_2.x ** 2 + v_2.y ** 2 + v_2.z ** 2)
        if np.sqrt(v_2.x ** 2 + v_2.y ** 2 + v_2.z ** 2) < 0.5 and fv.controller.control_function == emergency_v_ref:  # against small errors when stopping
            fv.controller.control_function = zero
        pos_f = fv.get_location()
        pos_prev = followers[j-1].get_location() if j > 0 else pos_l
        distance_logs[i, j] = pos_f.distance(pos_prev)
        trajectories[2 * i, j + 1], trajectories[2 * i + 1, j + 1] = pos_f.x, pos_f.y
    if i % 100 == 0:
        s_transform = followers[-1].get_transform()
        s_transform.location.z += 5
        s.spectator.set_transform(s_transform)
    try:
        time.sleep(0.01-(time.time()-tic))
    except ValueError:
        print("out of synch")

t = np.linspace(0, 70, 7000)
f, (plot1, plot2) = plt.subplots(1, 2)
plot2.set_aspect(1)
colors = plt.cm.get_cmap('hsv', len(followers)+1)
plot1.plot(t, log_lead, label="Lead", c=colors(0))
plot2.plot(trajectories[::2, 0], trajectories[1::2, 0], label="Lead")
for j, fv in enumerate(followers):
    plot1.plot(t, log_followers[:, j], label=f'Follower {j+1}', c=colors(j+1))
    plot1.plot(t, distance_logs[:, j], label=f'Gap {j + 1}', linestyle=":", c=colors(j+1))
    plot2.plot(trajectories[::2, j+1], trajectories[1::2, j+1], label=f'Follower {j+1}')
for wpt in p.lead_waypoints:
    plot2.scatter(wpt.transform.location.x, wpt.transform.location.y)
plot1.legend()
plot2.legend()
plt.show()