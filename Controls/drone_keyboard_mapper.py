# Controls/drone_keyboard_mapper.py

import math
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
# Track last action for debugging
last_action_label = 8  # Default: hover

def compute_action_label(forward, sideward, upward, yaw):
    """Compute the action label from the current inputs"""
    # Default hover state
    action_label = 8
    
    # Check if there's any significant movement
    if abs(forward) > 0.05 or abs(sideward) > 0.05 or abs(upward) > 0.05:
        # Determine the dominant direction
        max_dir = max(abs(forward), abs(sideward), abs(upward))
        if max_dir == abs(sideward):
            action_label = 0 if sideward > 0 else 1  # Right/Left
        elif max_dir == abs(forward):
            action_label = 2 if forward > 0 else 3  # Forward/Back
        else:
            action_label = 4 if upward > 0 else 5  # Up/Down
    elif abs(yaw) > 0.05:
        action_label = 6 if yaw > 0 else 7  # Turn Right/Left
        
    return action_label

def register_drone_keyboard_mapper(config):
    global controller
    controller = DroneControlManager()

    def on_key_pressed(key):
        if key in key_direction_map and key not in pressed_keys:
            pressed_keys.add(key)

    def on_key_released(key):
        if key in pressed_keys:
            pressed_keys.remove(key)

    def on_update(delta_time):
        global last_action_label
        
        # Early exit if no keys are pressed
        if not pressed_keys:
            # Only publish hover if last action wasn't hover
            if last_action_label != 8:
                EM.publish('keyboard/move', (0.0, 0.0, 0.0, 8))
                EM.publish('keyboard/rotate', (0.0, 8))
                last_action_label = 8
            return

        # Calculate direction based on pressed keys
        forward = 0
        sideward = 0
        upward = 0
        yaw = 0

        # Get move_step from config
        move_step = config.get('drone_move_step', 0.05)
        rotate_step = config.get('drone_rotate_step', 5.0)  # degrees
        
        # Single axis mode - only use the most recently pressed key
        single_axis_mode = config.get('single_axis_mode', False)
        if single_axis_mode and pressed_keys:
            # Use the most recent key in single axis mode
            newest_key = list(pressed_keys)[-1]
            if newest_key in key_direction_map:
                direction, factor = key_direction_map[newest_key]
                if direction == 'forward':
                    forward = factor
                elif direction == 'sideward':
                    sideward = factor
                elif direction == 'upward':
                    upward = factor
                elif direction == 'yaw':
                    yaw = factor
        else:
            # Normal multi-axis mode - process all keys
            for key in pressed_keys:
                direction, factor = key_direction_map[key]
                if direction == 'forward':
                    forward = factor
                elif direction == 'sideward':
                    sideward = factor
                elif direction == 'upward':
                    upward = factor
                elif direction == 'yaw':
                    yaw = factor

        # Compute action label based on movement
        action_label = compute_action_label(forward, sideward, upward, yaw)
        last_action_label = action_label  # Update last action

        # Publish movement with action label
        if forward or sideward or upward:
            EM.publish('keyboard/move', (sideward * move_step, forward * move_step, upward * move_step, action_label))
            print(f"Publishing move with action {action_label}: sideward={sideward}, forward={forward}, upward={upward}")
        else:
            # Still need to update the action label even when not moving
            EM.publish('keyboard/move', (0.0, 0.0, 0.0, action_label))
        
        if yaw:
            EM.publish('keyboard/rotate', (yaw * math.radians(rotate_step), action_label))
            print(f"Publishing rotate with action {action_label}: yaw={yaw}")
        else:
            # Still need to update the action label even when not rotating
            EM.publish('keyboard/rotate', (0.0, action_label))

    # Subscribe to keyboard events using the event manager
    EM.subscribe('keyboard/key_pressed', on_key_pressed)
    EM.subscribe('keyboard/key_released', on_key_released)
    EM.subscribe('simulation/frame', on_update)

    return controller
