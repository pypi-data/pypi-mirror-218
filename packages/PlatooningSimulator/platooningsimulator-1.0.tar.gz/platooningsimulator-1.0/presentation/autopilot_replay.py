import carla

client = carla.Client("localhost", 2000)
client.set_timeout(10000)
world = client.get_world()
settings = world.get_settings()
settings.synchronous = True
settings.fixed_delta_seconds = 0.02
world.apply_settings(settings)
client.set_replayer_time_factor(2.0)
client.replay_file("C:/Dev/Carla_logs/autopilot_recording_2.log", 0, 0, 127)