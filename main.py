# main.py

import time
import queue
import argparse
import multiprocessing
import tkinter as tk
import os
from Managers.depth_dataset_collector    import DepthDatasetCollector
from Utils.scene_utils                   import setup_scene_event_handlers
from Utils.config_utils                  import get_default_config
from Sensors.rgbd_camera_setup           import setup_rgbd_camera
from Controls.drone_keyboard_mapper      import register_drone_keyboard_mapper
from Core.event_manager                  import EventManager
from Managers.keyboard_manager           import KeyboardManager
from Managers.menu_system                import MenuSystem
from Managers.Connections.sim_connection import SimConnection
from Controls.drone_control_manager      import DroneControlManager
from Utils.lock_utils                    import sim_lock
from Managers.scene_manager              import get_scene_manager
from Controls.rc_controller              import rc_loop
from Utils.log_utils                     import get_logger, DEBUG_L1, DEBUG_L2, DEBUG_L3, LOG_LEVEL_DEBUG, LOG_LEVEL_INFO

# Global setup
EM = EventManager.get_instance()
KeyboardManager.get_instance()
SC = SimConnection.get_instance()
SM = get_scene_manager()
logger = get_logger()

# GUI prompt to select control mode
def select_control_mode():
    result = multiprocessing.Queue()

    def choose(mode):
        result.put(mode)
        window.destroy()

    window = tk.Tk()
    window.title("Select Control Mode")
    window.geometry("300x120")
    window.eval('tk::PlaceWindow . center')
    window.resizable(False, False)

    label = tk.Label(window, text="Choose control mode:", font=("Arial", 12))
    label.pack(pady=10)

    button_frame = tk.Frame(window)
    button_frame.pack()

    keyboard_button = tk.Button(button_frame, text="Keyboard", width=12, command=lambda: choose("keyboard"))
    keyboard_button.pack(side="left", padx=10)

    rc_button = tk.Button(button_frame, text="RC Controller", width=12, command=lambda: choose("rc"))
    rc_button.pack(side="right", padx=10)

    window.mainloop()
    return result.get()

def main():
    # Parse command-line arguments for logger configuration
    parser = argparse.ArgumentParser(description="Disaster Simulation Application")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--debug", type=int, choices=[1, 2, 3], default=1, 
                      help="Debug level (1=Basic, 2=Medium, 3=Verbose)")
    parser.add_argument("--log", action="store_true", help="Enable file logging")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    args = parser.parse_args()
    
    # Configure logger based on command-line arguments
    console_level = LOG_LEVEL_DEBUG if args.verbose else LOG_LEVEL_INFO
    debug_level = args.debug
    
    logger.configure(
        verbose=args.verbose,
        console_level=console_level,
        debug_level=debug_level,
        colored_output=not args.no_color
    )
    
    if args.log:
        # Enable file logging if requested
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"disaster_sim_{timestamp}.log"
        logger.configure_file_logging(enabled=True, level=LOG_LEVEL_DEBUG, filename=filename)
        logger.info("Main", f"File logging enabled: logs/{filename}")
    
    # Log application startup
    logger.info("Main", "Disaster Simulation application starting up")
    
    SC.connect()
    sim = SC.sim
    logger.info("Main", "Simulation connected successfully")

    # GUI: select control mode
    control_mode = select_control_mode()
    use_rc = control_mode == "rc"
    logger.info("Main", f"Control mode selected: {control_mode}")

    running = True

    def _on_app_quit(_):
        nonlocal running
        logger.info("Main", "Shutdown signal received, stopping simulation")
        running = False

    EM.subscribe('simulation/shutdown', _on_app_quit)
    sim_command_queue = queue.Queue()

    sim.setStepping(True)
    config = get_default_config()
    logger.debug_at_level(DEBUG_L2, "Main", f"Configuration loaded: {len(config)} settings")

    # Start RC controller or keyboard
    if use_rc:
        parent_conn, child_conn = multiprocessing.Pipe()
        rc_proc = multiprocessing.Process(target=rc_loop, args=(config, child_conn))
        rc_proc.start()
        logger.info("Main", "RC controller process started")

        # Subscribe to config updates to forward to RC controller
        def on_config_updated(key):
            if key == 'rc_sensitivity':
                sensitivity = config.get('rc_sensitivity', 5.0)
                parent_conn.send({'rc_sensitivity': sensitivity})
                logger.debug_at_level(DEBUG_L2, "Main", f"Sent RC sensitivity update: {sensitivity}")
        EM.subscribe('config/updated', on_config_updated)
    else:
        register_drone_keyboard_mapper(config)
        logger.info("Main", "Keyboard controls registered")
        parent_conn = None

    # Always activate control logic for both modes
    DroneControlManager()
    logger.info("Main", "Drone control manager initialized")

    # Register event handlers
    setup_scene_event_handlers()
    logger.debug_at_level(DEBUG_L1, "Main", "Scene event handlers registered")

    # Setup camera and dataset collector
    logger.info("Main", "Setting up RGBD camera...")
    cam_rgb, floating_view_rgb = setup_rgbd_camera(config)
    depth_collector = DepthDatasetCollector(
        cam_rgb,
        base_folder="data/depth_dataset",
        batch_size=config.get("batch_size", 100),
        save_every_n_frames=config.get("dataset_capture_frequency", 5),
        split_ratio=(0.8, 0.1, 0.1),
    )
    logger.info("Main", "Depth dataset collector initialized")
    
    # Store reference to depth_collector in SimConnection for access from UI
    SC.set_depth_collector(depth_collector)

    # Menu system
    logger.info("Main", "Initializing menu system...")
    menu_system = MenuSystem(config, sim_command_queue)
    logger.info("Main", "Menu system initialized")

    last_time = time.time()
    frame_count = 0
    last_fps_update = time.time()
    fps = 0

    # Main simulation loop
    logger.info("Main", "Starting main simulation loop")
    while running:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time
        
        # Calculate FPS every second
        frame_count += 1
        if current_time - last_fps_update >= 1.0:
            fps = frame_count / (current_time - last_fps_update)
            frame_count = 0
            last_fps_update = current_time
            logger.debug_at_level(DEBUG_L3, "Main", f"FPS: {fps:.2f}")

        with sim_lock() as locked:
            if locked:
                if hasattr(SM, 'random_object_manager') and SM.random_object_manager:
                    try:
                        SM.random_object_manager.update()
                    except Exception as e:
                        logger.error("Main", f"Error updating random objects: {e}")

                while not sim_command_queue.empty():
                    fn, args, kwargs = sim_command_queue.get()
                    try:
                        fn(*args, **kwargs)
                    except Exception as e:
                        logger.error("Main", f"Error executing simulation command: {e}")

                sim.handleVisionSensor(cam_rgb)

                # If using RC, inject move/rotate commands
                if parent_conn and parent_conn.poll():
                    move = parent_conn.recv()
                    logger.debug_at_level(DEBUG_L3, "Main", f"RC input: move={move[:3]}, rotate={move[3]}")
                    EM.publish('keyboard/move', move[:3])
                    EM.publish('keyboard/rotate', move[3])

                EM.publish('simulation/frame', delta_time)

        sim.step()

    # Shutdown cleanup
    logger.info("Main", "Starting shutdown procedures")
    
    if use_rc:
        logger.debug_at_level(DEBUG_L1, "Main", "Terminating RC controller process")
        rc_proc.terminate()
        rc_proc.join()

    SC.shutdown(depth_collector, floating_view_rgb)
    logger.info("Main", "Simulation disconnected and resources released")
    
    # Properly shut down the logger
    logger.info("Main", "Application shutdown complete")
    logger.shutdown()

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')  # Required on macOS
    main()
