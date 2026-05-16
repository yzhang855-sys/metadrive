from metadrive.component.static_object.traffic_object import TrafficCone, TrafficWarning
from metadrive.constants import TerminationState, DEFAULT_AGENT
from metadrive.envs.complex_env import ComplexEnv


def test_object_collision_detection(render=False):
    env = ComplexEnv(
        {
            "traffic_density": 0.0,
            "use_render": render,
            "crash_object_cost": 100,
            "crash_object_done": True,
            "debug": False,
            "vehicle_config": {"show_lidar": True}
        }
    )
    try:
        o, _ = env.reset()
        lane_index = (">>", ">>>", 0)
        lane = env.current_map.road_network.get_lane(lane_index)
        longitude = 22
        env.engine.object_manager.spawn_object(
            TrafficWarning,
            lane=env.current_map.road_network.get_lane(lane_index),
            position=lane.position(longitude, 0),
            heading_theta=lane.heading_theta_at(longitude)
        )
        lane_index = (">>", ">>>", 2)
        lane = env.current_map.road_network.get_lane(lane_index)
        env.engine.object_manager.spawn_object(
            TrafficCone,
            lane=env.current_map.road_network.get_lane(lane_index),
            position=lane.position(longitude, 0),
            heading_theta=lane.heading_theta_at(longitude)
        )
        crash_obj = False
        detect_obj = False
        for i in range(1, 100000 if render else 2000):
            o, r, tm, tc, info = env.step([0, 1])
            for obj in env.observations[DEFAULT_AGENT].detected_objects:
                if isinstance(obj, TrafficCone):
                    detect_obj = True
            if render:
                env.render()
            if info["cost"] == 100 and info[TerminationState.CRASH_OBJECT]:
                crash_obj = True
                break
        assert crash_obj and detect_obj, "Can not crash with object!"
    finally:
        env.close()


if __name__ == "__main__":
    test_object_collision_detection(render=False)