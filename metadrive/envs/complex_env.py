"""
ComplexEnv: a SafeMetaDriveEnv variant with complex obstacle scenarios.
Refactored from metadrive/tests/test_functionality/test_object_collision_detection.py
to consolidate all environment classes under metadrive/envs/.
"""
from metadrive.component.static_object.traffic_object import TrafficCone, TrafficWarning
from metadrive.component.vehicle.vehicle_type import LVehicle, SVehicle, XLVehicle
from metadrive.envs.safe_metadrive_env import SafeMetaDriveEnv
from metadrive.manager.object_manager import TrafficObjectManager


class ComplexObjectManager(TrafficObjectManager):
    """
    Manages complex obstacle layouts for the ComplexEnv scenario.
    The reset logic is decomposed into focused sub-methods for clarity
    and testability (breakdown_setup, part1, part2, part3, part4).
    """

    def breakdown_setup(self):
        """Spawn breakdown vehicles and warning sign at the start of the route."""
        lane = self.engine.current_map.road_network.graph[">>>"]["1C0_0_"][0]
        self.engine.object_manager.spawn_object(
            self.engine.traffic_manager.random_vehicle_type(),
            vehicle_config={"spawn_lane_index": lane.index, "spawn_longitude": 30}
        )
        self.engine.object_manager.accident_lanes.append(lane)

        lane_ = self.engine.current_map.road_network.graph[">>>"]["1C0_0_"][1]
        self.engine.object_manager.spawn_object(
            LVehicle,
            vehicle_config={"spawn_lane_index": lane_.index, "spawn_longitude": 30}
        )
        self.engine.object_manager.accident_lanes.append(lane_)

        longitude = 22
        self.engine.object_manager.spawn_object(
            TrafficWarning,
            lane=lane,
            position=lane.position(longitude, 0),
            heading_theta=lane.heading_theta_at(longitude),
        )

    def part1(self):
        """Place traffic cones and stalled vehicles on segment 1C0_1_ -> 2S0_0_."""
        lane = self.engine.current_map.road_network.graph["1C0_1_"]["2S0_0_"][2]
        pos = [
            (-20, lane.width / 3), (-15.6, lane.width / 4), (-12.1, 0),
            (-8.7, -lane.width / 4), (-4.2, -lane.width / 2),
            (-0.7, -lane.width * 3 / 4), (4.1, -lane.width), (7.3, -lane.width),
            (11.5, -lane.width), (15.5, -lane.width), (20.0, -lane.width),
            (23.2, -lane.width), (29.1, -lane.width), (32.9, -lane.width / 2),
            (37.0, 0), (40.0, lane.width / 2)
        ]
        for p in pos:
            self.engine.object_manager.spawn_object(
                TrafficCone,
                lane=lane,
                position=lane.position(p[0], p[1] + lane.width / 2),
                heading_theta=lane.heading_theta_at(p[0])
            )
        self.engine.object_manager.accident_lanes.append(lane)
        for v_long, v_t in zip([8, 14], [SVehicle, XLVehicle]):
            self.engine.object_manager.spawn_object(
                v_t,
                vehicle_config={"spawn_lane_index": lane.index, "spawn_longitude": v_long}
            )

    def part2(self):
        """Place traffic cones and warning signs on segment 3R0_0_ -> 3R0_1_."""
        lane = self.engine.current_map.road_network.graph["3R0_0_"]["3R0_1_"][0]
        self.engine.object_manager.accident_lanes.append(lane)
        pos = [
            (-20, lane.width / 3), (-15.6, lane.width / 4), (-12.1, 0),
            (-8.7, -lane.width / 4), (-4.2, -lane.width / 2),
            (-0.7, -lane.width * 3 / 4), (4.1, -lane.width), (7.3, -lane.width),
            (11.5, -lane.width), (15.5, -lane.width), (20.0, -lane.width),
            (23.2, -lane.width), (29.1, -lane.width), (32.9, -lane.width / 2),
            (37.0, 0), (40.0, lane.width / 2)
        ]
        for p in pos:
            p_ = (p[0] + 5, -p[1])
            self.engine.object_manager.spawn_object(
                TrafficCone,
                lane=lane,
                position=lane.position(p_[0], -p[1] - lane.width / 2),
                heading_theta=lane.heading_theta_at(p_[0])
            )
        for v_long in [14, 19]:
            self.engine.object_manager.spawn_object(
                self.engine.traffic_manager.random_vehicle_type(),
                vehicle_config={"spawn_lane_index": lane.index, "spawn_longitude": v_long}
            )
        for longitude in [-35, -60]:
            self.engine.object_manager.spawn_object(
                TrafficWarning,
                lane=lane,
                position=lane.position(longitude, 0),
                heading_theta=lane.heading_theta_at(longitude)
            )

    def part3(self):
        """Place traffic cones and stalled vehicles on segment 4C0_0_ -> 4C0_1_."""
        lane = self.engine.current_map.road_network.graph["4C0_0_"]["4C0_1_"][2]
        self.engine.object_manager.accident_lanes.append(lane)
        pos = [
            (-12.1, 0), (-8.7, -lane.width / 4), (-4.2, -lane.width / 2),
            (-0.7, -lane.width * 3 / 4), (4.1, -lane.width), (7.3, -lane.width),
            (11.5, -lane.width), (15.5, -lane.width), (20.0, -lane.width),
            (23.2, -lane.width), (29.1, -lane.width), (32.9, -lane.width / 2),
            (37.0, 0), (40.0, lane.width / 2)
        ]
        for p in pos:
            p_ = (p[0] + 5, p[1] * 3.5 / 3)
            self.engine.object_manager.spawn_object(
                TrafficCone,
                lane=lane,
                position=lane.position(p_[0], p[1] + lane.width / 2),
                heading_theta=lane.heading_theta_at(p_[0])
            )
        for v_long in [14, 19]:
            self.engine.object_manager.spawn_object(
                self.engine.traffic_manager.random_vehicle_type(),
                vehicle_config={"spawn_lane_index": lane.index, "spawn_longitude": v_long}
            )

    def part4(self):
        """Mark accident lane on segment 4C0_1_ -> 5R0_0_ (reserved for future obstacles)."""
        lane = self.engine.current_map.road_network.graph["4C0_1_"]["5R0_0_"][0]
        self.engine.object_manager.accident_lanes.append(lane)

    def reset(self):
        """Reset the object manager and populate all obstacle sub-scenarios."""
        ret = super(ComplexObjectManager, self).reset()
        self.breakdown_setup()
        self.part1()
        self.part2()
        self.part3()
        self.part4()
        return ret


class ComplexEnv(SafeMetaDriveEnv):
    """
    A SafeMetaDriveEnv variant featuring complex multi-obstacle scenarios.
    Refactored from test_object_collision_detection.py into the envs package
    to consolidate all environment classes in one location.
    """

    def default_config(self):
        config = super(ComplexEnv, self).default_config()
        config.update({
            "num_scenarios": 1,
            "traffic_density": 0.05,
            "start_seed": 5,
            "accident_prob": 0.0,
            "debug_physics_world": False,
            "debug": False,
            "map": "CSRCR"
        })
        return config

    def setup_engine(self):
        super(ComplexEnv, self).setup_engine()
        self.engine.register_manager("object_manager", ComplexObjectManager())