# main.py

import time
from Utils.scene_utils import start_sim_if_needed
from Controls.camera_setup import setup_drone_camera
from Controls.camera_view import CameraView
from Controls.keyboard_manager import KeyboardManager

def show_menu():
    print("\n[Menu]")
    print("  1 - Create rectangle")
    print("  2 - Erase rectangle")
    print("  q - Quit")
    print("\nPress Enter to return to movement control mode.\n")

def create_rectangle(sim, target_handle, size, position, color):
    rectangle_handle = sim.createPrimitiveShape(sim.primitiveshape_cuboid, size, 0)
    sim.setObjectPosition(rectangle_handle, target_handle, position)
    sim.setShapeColor(rectangle_handle, None, sim.colorcomponent_ambient_diffuse, color)
    sim.setObjectAlias(rectangle_handle, "SimpleRectangle")
    print(f"[Main] Rectangle created with size {size} at position {position}")
    return rectangle_handle

def main():
    sim = start_sim_if_needed()
    print("[Main] Simulation started.")
    print("[Main] Press Enter to access menu options.")

    sim.setStepping(True)

    camera_handle = setup_drone_camera(sim)
    target_handle = sim.getObject('/target')

    camera_view = CameraView(sim, camera_handle)
    camera_view.start()

    keyboard_manager = KeyboardManager(sim, target_handle)
    
    # Rectangle configuration - modify these values as needed
    rect_size = [1.5, 1.5, 1.5]  # width, length, height
    rect_position = [0, 0, 0.15]   # x, y, z position relative to target
    rect_color = [0.2, 0.6, 0.8]   # RGB color (light blue)
    
    # Initialize rectangle handle to None (no rectangle at start)
    rectangle_handle = None

    try:
        running = True
        while running:
            keyboard_manager.process_keys()

            if keyboard_manager.in_typing_mode():
                show_menu()
                
                # Temporarily disable stepping to allow input
                sim.setStepping(False)
                
                try:
                    # Reset terminal state for input
                    command = input(">> ").strip().lower()
                except EOFError:
                    command = ""
                    
                # Re-enable stepping
                sim.setStepping(True)
                keyboard_manager.finish_typing(command)
                
                # Process command immediately after input
                if command == '1':
                    sim.acquireLock()
                    if rectangle_handle is None:
                        # Create rectangle
                        rectangle_handle = create_rectangle(sim, target_handle, rect_size, rect_position, rect_color)
                    else:
                        print("[Main] Rectangle already exists.")
                    sim.releaseLock()
                elif command == '2':
                    sim.acquireLock()
                    if rectangle_handle is not None:
                        sim.removeObject(rectangle_handle)
                        rectangle_handle = None
                        print("[Main] Rectangle erased.")
                    else:
                        print("[Main] No rectangle to erase.")
                    sim.releaseLock()
                elif command == 'q':
                    print("[Main] Quit requested.")
                    running = False
                elif command:
                    print(f"[Main] Unknown command: '{command}'")

            # Update simulation
            camera_view.update()
            for _ in range(3):
                sim.step()
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\n[Main] Exiting on Ctrl-C.")

    keyboard_manager.stop()
    camera_view.close()

    # Graceful shutdown
    try:
        sim.disconnect()
    except Exception:
        pass  # Sometimes sim already closed

    print("[Main] Simulation stopped.")

if __name__ == '__main__':
    main()
