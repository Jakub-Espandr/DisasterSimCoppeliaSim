# Controls/rc_controller.py

import pygame
import time
import multiprocessing
from Core.event_manager import EventManager
from Utils.log_utils import get_logger, DEBUG_L1, DEBUG_L2, DEBUG_L3

EM = EventManager.get_instance()
logger = get_logger()

def rc_loop(config, conn):
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        logger.warning("RC", "No joystick detected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    logger.info("RC", f"Using: {joystick.get_name()}")

    move_step = config.get('move_step', 0.2)
    rotate_step = config.get('rotate_step_deg', 10.0)
    sensitivity = config.get('rc_sensitivity', 10.0)

    def deadzone(val, threshold=0.1):
        return val if abs(val) > threshold else 0.0

    while True:
        try:
            # Check for config updates from the pipe
            if conn.poll():
                data = conn.recv()
                if isinstance(data, dict) and 'rc_sensitivity' in data:
                    sensitivity = data['rc_sensitivity']
                    logger.info("RC", f"Sensitivity updated to: {sensitivity}")
                    continue

            pygame.event.pump()
            pitch = -joystick.get_axis(1)
            roll = joystick.get_axis(0)
            throttle = joystick.get_axis(2)
            yaw = joystick.get_axis(3)

            # Debug output at high verbosity level
            logger.debug_at_level(DEBUG_L3, "RC", f"pitch={pitch:.2f}, roll={roll:.2f}, throttle={throttle:.2f}, yaw={yaw:.2f}")

        except Exception as e:
            logger.error("RC", f"Error reading axes: {e}")
            continue

        forward = -deadzone(pitch) * move_step * sensitivity
        sideward = deadzone(roll) * move_step * sensitivity
        upward = deadzone(throttle) * move_step * sensitivity
        def expo_curve(x, expo=0.5):
            return x * abs(x) ** expo

        yaw_rate = -deadzone(yaw) * rotate_step * 0.07  # 7% of normal

        conn.send((sideward, forward, upward, yaw_rate))

        time.sleep(0.05)
