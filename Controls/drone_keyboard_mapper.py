# Controls/drone_keyboard_mapper.py

from Core.event_manager import EventManager
from Managers.keyboard_manager import KeyboardManager

from Controls.drone_control_manager import DroneControlManager
controller = None

EM = EventManager.get_instance()
KM = KeyboardManager.get_instance()

# Key mapping → direction
key_direction_map = {
    'w': ('forward', 1),
    's': ('forward', -1),
    'a': ('sideward', -1),
    'd': ('sideward', 1),
    ' ': ('upward', 1),
    'z': ('upward', -1),
    'q': ('yaw', 1),
    'e': ('yaw', -1),
}

# Track pressed keys
pressed_keys = set()

def register_drone_keyboard_mapper(config):
    global controller
    controller = DroneControlManager()

    def on_key_pressed(key):
        if KM.in_typing_mode():
            return

        if key in key_direction_map:
            pressed_keys.add(key)
            
        elif key == 'y':
            EM.publish('keyboard/move', (0.0, 0.0, 0.0))
            EM.publish('keyboard/rotate', 0.0)


    def on_key_released(key):
        if key in pressed_keys:
            pressed_keys.discard(key)





    def on_simulation_frame(_):
        forward = sideward = upward = yaw = 0
        for key in pressed_keys:
            if key not in key_direction_map:
                continue
            direction, sign = key_direction_map[key]
            if direction == 'forward':
                forward += sign
            elif direction == 'sideward':
                sideward += sign
            elif direction == 'upward':
                upward += sign
            elif direction == 'yaw':
                yaw += sign

        # Apply single-axis movement restriction if enabled
        if config.get("single_axis_mode", False):
            # Determine which input has the largest magnitude
            max_input = max(abs(forward), abs(sideward), abs(yaw), abs(upward))
            
            # Only allow the axis with the largest input, zero out all others
            if max_input > 0:
                if abs(forward) == max_input:  # Forward/backward has priority
                    sideward = 0
                    upward = 0
                    yaw = 0
                elif abs(sideward) == max_input:  # Left/right has priority
                    forward = 0
                    upward = 0
                    yaw = 0
                elif abs(yaw) == max_input:  # Rotation has priority
                    forward = 0
                    sideward = 0
                    upward = 0
                elif abs(upward) == max_input:  # Up/down has priority
                    forward = 0
                    sideward = 0
                    yaw = 0

        move_step = config.get('move_step', 0.2)
        rotate_step = config.get('rotate_step_deg', 15.0)
        import math

        if pressed_keys:
            # Keys are held – apply smooth movement
            if forward or sideward or upward:
                EM.publish('keyboard/move', (sideward * move_step, forward * move_step, upward * move_step))
            if yaw:
                EM.publish('keyboard/rotate', yaw * math.radians(rotate_step))
        else:
            # No key is pressed – stop drone just like pressing "y"
            EM.publish('keyboard/move', (0.0, 0.0, 0.0))
            EM.publish('keyboard/rotate', 0.0)

    EM.subscribe('keyboard/key_pressed', on_key_pressed)
    EM.subscribe('keyboard/key_released', on_key_released)
    EM.subscribe('simulation/frame', on_simulation_frame)
