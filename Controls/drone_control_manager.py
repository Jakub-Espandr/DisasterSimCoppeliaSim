# Controls/drone_control_manager.py

from Controls.drone_movement_transformer import DroneMovementTransformer
from Core.event_manager import EventManager
from Utils.log_utils import get_logger, DEBUG_L1, DEBUG_L2, DEBUG_L3

EM = EventManager.get_instance()

class DroneControlManager:
    def __init__(self):
        self._forward = 0.0
        self._sideward = 0.0
        self._upward = 0.0
        self._yaw_rate = 0.0
        
        # Initialize logger
        self.logger = get_logger()
        
        # Add input buffer to handle rapid inputs
        self._input_buffer = []
        self._max_buffer_size = 3  # Maximum number of inputs to buffer
        
        # Track if we're currently processing scene creation
        self._scene_creation_active = False

        self.camera_movement_controller = DroneMovementTransformer()

        EM.subscribe('keyboard/move', self._on_move)
        EM.subscribe('keyboard/rotate', self._on_rotate)
        EM.subscribe('simulation/frame', self._update)
        
        # Track scene creation status to optimize performance
        EM.subscribe('scene/start_creation', self._on_scene_creation_start)
        EM.subscribe('scene/creation/completed', self._on_scene_creation_completed)
        EM.subscribe('scene/creation/canceled', self._on_scene_creation_completed)

    def _on_move(self, delta):
        # Handle both formats: (dx, dy, dz) and (dx, dy, dz, action_label)
        if isinstance(delta, (tuple, list)):
            if len(delta) >= 3:
                dx, dy, dz = delta[:3]
                
                # Prioritize input processing during scene creation
                if self._scene_creation_active:
                    # Apply inputs immediately with higher priority
                    self._sideward = dx
                    self._forward = dy
                    self._upward = dz
                else:
                    # Normal operation - buffer inputs if needed
                    self._sideward = dx
                    self._forward = dy
                    self._upward = dz
                
                # Store action label if available (4-tuple)
                if len(delta) == 4:
                    action_label = delta[3]
                    # Log for debugging
                    self.logger.debug_at_level(DEBUG_L3, "DroneControl", f"Move with action label: {action_label}")

    def _on_rotate(self, delta):
        # Handle both formats: numeric value and (delta_val, action_label)
        if isinstance(delta, (tuple, list)) and len(delta) == 2:
            delta_val, action_label = delta
            self._yaw_rate = delta_val  # Direct assignment for more responsive rotation
            # Log for debugging
            self.logger.debug_at_level(DEBUG_L3, "DroneControl", f"Rotate with action label: {action_label}")
        else:
            self._yaw_rate = delta  # Direct assignment for more responsive rotation
    
    def _on_scene_creation_start(self, _):
        self._scene_creation_active = True
        self.logger.debug_at_level(DEBUG_L2, "DroneControl", "Scene creation started - optimizing control response")
    
    def _on_scene_creation_completed(self, _):
        self._scene_creation_active = False
        self.logger.debug_at_level(DEBUG_L2, "DroneControl", "Scene creation completed - returning to normal control mode")

    def _update(self, dt):
        self.camera_movement_controller.update(
            self._forward,
            self._sideward,
            self._upward,
            self._yaw_rate,
            dt
        )

        # Reset rotation rate immediately for responsive control
        self._yaw_rate = 0.0
        
        # Always use gradual decay for smoother movement regardless of scene creation status
        # This ensures consistent movement behavior before and after scene creation
        decay_rate = 0.7  # Higher value = slower decay
        self._forward *= decay_rate
        self._sideward *= decay_rate
        self._upward *= decay_rate
        
        # Reset to zero if below threshold
        if abs(self._forward) < 0.01: self._forward = 0.0
        if abs(self._sideward) < 0.01: self._sideward = 0.0
        if abs(self._upward) < 0.01: self._upward = 0.0

    def reset_controls(self):
        self._forward = 0.0
        self._sideward = 0.0
        self._upward = 0.0
        self._yaw_rate = 0.0
