# Utils/scene_utils.py

from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

# Simulation state constants
SIMULATION_STOPPED = 0
SIMULATION_PAUSED = 1
SIMULATION_ADVANCING_FIRSTAFTERSTOP = 2
SIMULATION_ADVANCING_RUNNING = 3
SIMULATION_ADVANCING_LASTBEFOREPAUSE = 4
SIMULATION_ADVANCING_FIRSTAFTERPAUSE = 5
SIMULATION_ADVANCING_ABOUTTOSTOP = 6
SIMULATION_ADVANCING_LASTBEFORESTOP = 7

def start_sim_if_needed(timeout_sec=2.5):
    """
    Connects to CoppeliaSim and starts the simulation if it is stopped.
    Returns (client, sim).
    """
    client = RemoteAPIClient()
    sim = client.require('sim')
    sim_state = sim.getSimulationState()

    if sim_state == SIMULATION_ADVANCING_RUNNING:
        print("[SceneUtils] Simulation already running.")
        return sim

    if sim_state == SIMULATION_STOPPED:
        print("[SceneUtils] Starting simulation...")
        sim.startSimulation()
        start_time = time.time()
        while True:
            try:
                if sim.getSimulationState() == SIMULATION_ADVANCING_RUNNING:
                    print("[SceneUtils] Simulation started (confirmed running).")
                    return sim
            except Exception:
                pass
            if time.time() - start_time > timeout_sec:
                current_state = sim.getSimulationState()
                if current_state == SIMULATION_STOPPED:
                    print("[SceneUtils] Warning: Start timeout. Still reporting stopped, assuming running.")
                else:
                    print(f"[SceneUtils] Warning: Start timeout. State={current_state}. Proceeding anyway.")
                return sim
            time.sleep(0.05)
    else:
        print(f"[SceneUtils] Unexpected state {sim_state}. Continuing.")
        return sim
