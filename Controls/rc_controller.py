# Controls/rc_controller.py

import pygame
import time
import multiprocessing
from Core.event_manager import EventManager
from Utils.log_utils import get_logger, DEBUG_L1, DEBUG_L2, DEBUG_L3

EM = EventManager.get_instance()
logger = get_logger()

def rc_loop(config, conn):
    """
    Main loop for RC controller input processing.
    Runs in a separate process.
    """
    # Initialize pygame
    pygame.init()
    pygame.joystick.init()
    
    # Initialize variables
    sensitivity = config.get('rc_sensitivity', 1.0)  # Default to 1.0
    deadzone_threshold = config.get('rc_deadzone', 0.1)
    yaw_sensitivity = config.get('rc_yaw_sensitivity', 0.15)
    mappings = config.get('rc_mappings', {})
    single_axis_mode = config.get('single_axis_mode', False)
    
    # Variables to track last sent values to minimize unnecessary updates
    last_x_axis = last_y_axis = last_z_axis = last_yaw = 0.0
    
    # Throttle update rate - controls how many position updates to skip
    update_counter = 0
    update_every = 1  # Send every update by default
    
    # Timestamp tracking for adaptive timing
    last_time = time.time()
    frame_time_avg = 0.01  # Initialize with a reasonable value
    
    # Try to initialize joystick
    try:
        if pygame.joystick.get_count() == 0:
            logger.warning("RC", "No joystick detected.")
            return
            
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        logger.info("RC", f"Using: {joystick.get_name()}")
    except pygame.error:
        logger.error("RC", "Failed to initialize joystick")
        return
    
    # Log the initial controller configuration
    logger.info("RC", f"Controller started with sensitivity: {sensitivity}, deadzone: {deadzone_threshold}, yaw sensitivity: {yaw_sensitivity}")
    
    running = True
    while running:
        try:
            # Start timing this frame's processing
            frame_start = time.time()
            
            # Process pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Check for config updates from parent process
            if conn.poll():
                data = conn.recv()
                if isinstance(data, dict):
                    for key, value in data.items():
                        if key == 'rc_sensitivity':
                            sensitivity = value
                            logger.info("RC", f"Sensitivity updated to: {sensitivity}")
                        elif key == 'rc_deadzone':
                            deadzone_threshold = value
                            logger.info("RC", f"Deadzone updated to: {deadzone_threshold}")
                        elif key == 'rc_yaw_sensitivity':
                            yaw_sensitivity = value
                            logger.info("RC", f"Yaw sensitivity updated to: {yaw_sensitivity}")
                        elif key == 'rc_mappings':
                            mappings = value
                            logger.info("RC", f"Mappings updated: {mappings}")
                        elif key == 'single_axis_mode':
                            single_axis_mode = value
                            logger.info("RC", f"Single-axis mode updated to: {single_axis_mode}")
                    continue
            
            # Get joystick inputs with proper error handling
            try:
                # Get axis values with deadzone applied
                x_axis = get_axis_value(joystick, mappings.get('roll', {}).get('axis', 0), 
                                       deadzone_threshold, mappings.get('roll', {}).get('invert', False))
                y_axis = get_axis_value(joystick, mappings.get('pitch', {}).get('axis', 1), 
                                       deadzone_threshold, mappings.get('pitch', {}).get('invert', False))
                z_axis = get_axis_value(joystick, mappings.get('throttle', {}).get('axis', 2), 
                                       deadzone_threshold, mappings.get('throttle', {}).get('invert', False))
                yaw = get_axis_value(joystick, mappings.get('yaw', {}).get('axis', 3), 
                                    deadzone_threshold, mappings.get('yaw', {}).get('invert', False))
                
                # Apply sensitivity
                x_axis *= sensitivity
                y_axis *= sensitivity
                z_axis *= sensitivity
                yaw *= yaw_sensitivity
                
                # Apply single-axis movement restriction if enabled
                if single_axis_mode:
                    # Determine which axis has the largest input (absolute value)
                    max_input = max(abs(y_axis), abs(x_axis), abs(yaw), abs(z_axis))
                    
                    # Only allow the axis with the largest input, zero out all others
                    if max_input > deadzone_threshold:
                        if abs(y_axis) == max_input:  # Pitch (forward/backward) has priority
                            x_axis = 0
                            z_axis = 0
                            yaw = 0
                        elif abs(x_axis) == max_input:  # Roll (left/right) has priority
                            y_axis = 0
                            z_axis = 0
                            yaw = 0
                        elif abs(yaw) == max_input:  # Yaw (rotation) has priority
                            x_axis = 0
                            y_axis = 0
                            z_axis = 0
                        elif abs(z_axis) == max_input:  # Throttle (up/down) has priority
                            x_axis = 0
                            y_axis = 0
                            yaw = 0
                
                # Always send updates when values change significantly
                # Use a smaller threshold to detect changes
                should_update = (
                    abs(x_axis - last_x_axis) > 0.005 or
                    abs(y_axis - last_y_axis) > 0.005 or
                    abs(z_axis - last_z_axis) > 0.005 or
                    abs(yaw - last_yaw) > 0.005
                )
                
                # Also send periodic updates even without changes (reduced from previous)
                update_counter += 1
                if update_counter >= 2:  # Send at least every 2nd frame
                    should_update = True
                    update_counter = 0
                
                if should_update:
                    conn.send([x_axis, y_axis, z_axis, yaw])
                    last_x_axis, last_y_axis, last_z_axis, last_yaw = x_axis, y_axis, z_axis, yaw
                
                # Debug output at high verbosity level
                logger.debug_at_level(DEBUG_L3, "RC", f"x={x_axis:.2f}, y={y_axis:.2f}, z={z_axis:.2f}, yaw={yaw:.2f}")
                
            except Exception as e:
                logger.error("RC", f"Error reading joystick axes: {e}")
                time.sleep(0.05)  # Reduced delay before retrying
                continue
            
            # Calculate frame processing time
            frame_end = time.time()
            frame_time = frame_end - frame_start
            
            # Use a moving average for frame time to make sleep times more stable
            frame_time_avg = 0.9 * frame_time_avg + 0.1 * frame_time
            
            # Reduced sleep time for more responsive control
            # Minimum 5ms, target 20ms total cycle time (increased frequency)
            sleep_time = max(0.005, 0.02 - frame_time_avg)
            time.sleep(sleep_time)
            
        except Exception as e:
            logger.error("RC", f"Error in RC controller loop: {e}")
            time.sleep(0.05)  # Reduced delay before retrying
            continue
    
    # Clean up
    pygame.quit()

def get_axis_value(joystick, axis, deadzone, invert=False):
    if axis is None:
        return 0.0
        
    if isinstance(axis, (int, float)) and axis < joystick.get_numaxes():
        value = joystick.get_axis(axis)
        if abs(value) <= deadzone:
            return 0.0
        # Scale the value to maintain smooth range after deadzone
        scaled_value = (value - (deadzone if value > 0 else -deadzone)) / (1.0 - deadzone)
        if invert:
            scaled_value = -scaled_value
        return scaled_value
    return 0.0
