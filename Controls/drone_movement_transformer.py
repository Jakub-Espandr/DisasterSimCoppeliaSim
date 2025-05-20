# Controls/drone_movement_transformer.py

import math
from Managers.Connections.sim_connection import SimConnection
from Utils.log_utils import get_logger, DEBUG_L1, DEBUG_L2, DEBUG_L3

SC = SimConnection.get_instance()
logger = get_logger()

class DroneMovementTransformer:
    def __init__(self):
        self.target_handle = SC.sim.getObject('/target')
        self.drone_base = SC.sim.getObject('/Quadcopter/base')
        self.logger = get_logger()
        
        # Track last update time for consistent movement regardless of frame rate
        self.last_update_time = 0
        
        # Movement smoothing variables
        self.movement_smoothing = 0.7  # Lower values = more responsive (0-1)
        self.current_dx = 0
        self.current_dy = 0
        self.current_dz = 0
        self.current_yaw_rate = 0

    def update(self, forward, sideward, upward, yaw_rate, dt):
        # Get current rotation around Z axis (yaw)
        yaw = SC.sim.getObjectOrientation(self.drone_base, -1)[2]

        # Convert to world coordinates
        dx = -forward * math.cos(yaw) - sideward * math.sin(yaw)
        dy = -forward * math.sin(yaw) + sideward * math.cos(yaw)
        dz = upward
        
        # Apply smoothing for more natural movement
        # When inputs are zero, reduce smoothing for quicker stopping
        if abs(dx) < 0.01 and abs(dy) < 0.01 and abs(dz) < 0.01:
            stop_smoothing = 0.5  # Faster stop response
            self.current_dx = self.current_dx * stop_smoothing
            self.current_dy = self.current_dy * stop_smoothing
            self.current_dz = self.current_dz * stop_smoothing
        else:
            # Normal smoothing for movement
            self.current_dx = self.current_dx * self.movement_smoothing + dx * (1.0 - self.movement_smoothing)
            self.current_dy = self.current_dy * self.movement_smoothing + dy * (1.0 - self.movement_smoothing)
            self.current_dz = self.current_dz * self.movement_smoothing + dz * (1.0 - self.movement_smoothing)
            
        # Apply smoothing to rotation (less smoothing for more responsive turning)
        rotation_smoothing = 0.5  # More responsive rotation
        self.current_yaw_rate = self.current_yaw_rate * rotation_smoothing + yaw_rate * (1.0 - rotation_smoothing)
        
        # Use smoothed values for movement
        dx = self.current_dx
        dy = self.current_dy
        dz = self.current_dz
        yaw_rate = self.current_yaw_rate

        # Calculate new position
        current_pos = SC.sim.getObjectPosition(self.target_handle, -1)
        new_pos = [
            current_pos[0] + dx * dt,
            current_pos[1] + dy * dt,
            current_pos[2] + dz * dt
        ]

        SC.sim.setObjectPosition(self.target_handle, -1, new_pos)

        # Calculate new rotation
        current_ori = SC.sim.getObjectOrientation(self.target_handle, -1)
        new_yaw = current_ori[2] + yaw_rate * dt
        SC.sim.setObjectOrientation(self.target_handle, -1, [current_ori[0], current_ori[1], new_yaw])

        # Debug output (optional)
        self.logger.debug_at_level(DEBUG_L3, "Movement", f"dx={dx:.3f}, dy={dy:.3f}, dz={dz:.3f}, yaw_rate={yaw_rate:.3f}")
