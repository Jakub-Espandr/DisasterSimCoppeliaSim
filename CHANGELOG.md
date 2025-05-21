## [V.1.4.0B] - HyperDrive Pathway - 2025-05-21

### Added
**- Enhanced Configuration Management:**
- Added ability to save configuration files to custom locations with user-defined names
- Implemented directory browser for configuration file saving and loading
- Set Config folder as default location for all settings files (same as rc_mapping.json and rc_settings.json)
- Added full path display in configuration dialogs for better clarity

### Fixed
**- Keyboard Movement Controls:**
- Fixed critical issue where movement controls (forward/sideward/up) stopped working after saving settings
- Ensured movement speed values are properly preserved when switching between tabs or saving configuration
- Improved decimal precision for movement speed to support values like 0.05
- Enhanced configuration synchronization between UI and internal settings

---

## [V.1.4.0] - HyperDrive Pathway - 2025-05-21

### Added
**- Enhanced scrolling experience:**
- Implemented advanced cross-platform trackpad scrolling support
- Added smooth scrolling with platform-specific optimizations alongside traditional scrollbar

**- Improved UI responsiveness:**
- Enhanced performance for macOS, Windows, and Linux platforms

### Fixed
**- Dataset action recording:**
- Fixed issue where dataset wasn't properly recording actions
- Ensured all control inputs are correctly logged in dataset captures

**- Control initialization:**
- Fixed issues with initial values for RC controller and keyboard
- Ensured proper initialization of control parameters on application startup

---

## [V.1.3.3C] - HyperDrive Insight - 2025-05-20

###Added
**- Improved batch management safety:**
- Added safety mechanism to only allow batch removal when the simulation is stopped
- Prevents potential data corruption from removing batches during active simulation

###Fixed
**- Fixed batch counter synchronization:**
- Ensured batch counters are properly synchronized with the file system when creating a new scene
- Fixed issue where new batches might not have the correct sequential numbering

---

## [V.1.3.3B] - HyperDrive Insight - 2025-05-19

###Added
**- Batch management in Dataset tab:** 
- Implemented side-by-side display of current batch and scene batch numbers
- Added refresh button to update batch information display
- Created "Remove Batches From Current Scene" button with confirmation dialog
- Improved safety by only allowing batch removal when simulation is not running

**- Option to keep or remove fallen trees:** 
- Added a toggle button in the configuration tab to allow users to choose whether fallen trees should be kept on the ground or removed during tree respawning

###Changed
**- Streamlined Dataset interface:** 
- Eliminated entire Configuration section from Dataset tab
- Updated help documentation to match actual application functionality

**- Enhanced object management:** 
- Modified RandomObjectManager to handle birds and falling trees separately
- Improved memory management by isolating tree respawn from bird lifecycle

###Fixed
**- Fixed bird respawning issue:** 
- Birds no longer respawn when falling trees are regenerated
- Corrected undefined batch_counter_file variable
- Improved error handling for batch file operations

**- Fixed tree cleanup bug:**
- Ensured old trees are properly deleted before spawning new ones
- Implemented proper tree handle tracking and cleanup process

---

## [V.1.3.3] - HyperDrive Insight - 2025-05-19

###Added
**- Depth Data Visualization in Main App:**  
- Integrated button to load Depth Data Visualization Tool from main app (dataset tab)

**- Preset Change Inspection Feature:** 
- Implemented a system to inspect and highlight changes when loading a saved preset
- Added automatic comparison of current and loaded configuration values
- Visual indicators now display what settings are newly applied or differ from the current session

###Changed
**- Preset Handling Enhancements:**  
- Improved loading logic to ensure all relevant modules are updated before scene manipulation
- Added internal tracking of preset states to avoid redundant application of unchanged values

###Fixed
**- Object Creation After Preset Load:**  
- Fixed issue where objects were not properly re-initialized after loading a new preset
- Resolved inconsistency in object spawning caused by outdated references after reload
- Ensured complete re-sync of scene entities with loaded configuration parameters

---

## [V.1.3.2B] - HyperDrive Pulse - 2025-05-17

### Fixed
- Hiding target for camera view and RGBD data collection.

---

## [V.1.3.2] - HyperDrive Pulse - 2025-05-16

### Added
**- Enhanced RC Controller Visualization:**  
- Added visual joystick representation in the RC Controller test window
- Implemented real-time visualization of stick positions with color-coded indicators
- Created dedicated joystick visualizer component for consistent UI across the application
- Added support for displaying both Pitch/Roll and Throttle/Yaw movements simultaneously

**- Improved Single-Axis Movement Mode:**  
- Implemented single-axis movement with strict one-axis-at-a-time operation
- Added logic to only allow the axis with the largest input to be active

**- RC Controller Settings Enhancements:**  
- Added adaptive display formatting for sensitivity values based on magnitude
- Improved RC Mapping Wizard with visual feedback during axis mapping

**- UI Improvements:**  
- Enhanced progress bar lengths for better visualization of control inputs
- Updated Help tab with comprehensive documentation of all features

### Changed
**- RC Controller Loop Implementation:**  
- Added sophisticated adaptive timing system with moving average for frame time
- Implemented dynamic sleep times based on system load for better responsiveness
- Added optimization to only send updates when values change significantly
- Enhanced error handling with comprehensive try/except blocks

### Fixed
**- RC Controller Responsiveness:**  
- Fixed lag between joystick movement and drone response
- Resolved issue with RC controller mappings structure causing TypeError
- Added proper error handling for axis values in get_axis_value function

### Performance
**- Optimized RC Controller Processing:**  
- Implemented frame time tracking with moving average for stable timing
- Added dynamic sleep calculation based on processing load
- Reduced unnecessary updates with value change detection
- Enhanced error recovery with small delays before retrying after errors

---

## [V.1.3.1] - HyperDrive Sync - 2025-05-11

### Added
**- Automatic Loading of RC Controller Settings:**  
- The application now automatically loads saved RC controller settings and mappings at startup.

**- Immediate Application of RC Settings:**  
- RC-related settings are immediately sent to the controller process upon startup.

**- New Control Setup Tab:**  
- A new tab in the GUI allows users to configure both keyboard and RC controller settings, including options to **preview real time axis movement of the controller.**

**- GUI Axis Mapping Wizard:**  
- A new GUI wizard assists users in mapping their RC joystick to match the correct control behavior.

### Changed
**- Scene Clearing Improvements:**  
- Enhanced the scene clearing process to ensure all objects are properly removed, with improved error handling and logging.

**- UI Enhancements:**  
- Improved confirmation dialog styling and button text centering.  
- Application title in the window title bar and Help tab.

### Fixed
**- Reduced Delay in RC Controller Response:**  
- Reduced the delay between stick movement and target movement in the simulation, enhancing responsiveness.

**- Error Handling:**  
- Improved error handling across various methods to prevent crashes and ensure graceful shutdowns.

### Performance
**- Logging Enhancements:**  
- Added detailed logging for loading RC settings and mappings, improving visibility into the configuration process.

**- Resource Management:**  
- Enhanced shutdown procedures to ensure all resources are released properly, preventing memory leaks and ensuring clean application exits.

---

## [V.1.3.0] - HyperDrive Navigator - 2025-05-10

### Added
**- Added UI keyboard control capabilities:**  
- Direct keyboard input through the application window  
- Control status indicator in Status tab  
- Proper focus handling for seamless control switching

**- Added RC joystick controller documentation and support**

**- Added comprehensive application icon support:**  
- Platform-specific icon loading for macOS and Windows  
- Error handling for missing icon files  
- Resolution-appropriate icon rendering

**- Added tools for showing datasets, enhancing data visualization and analysis capabilities:**  
- Preview pane for captured depth images  
- Basic preprocessing tools  
- Quick-access export functionality

**- Enhanced Help tab with expanded information and improved organization.**

### Changed
- Completely redesigned the user interface for a more modern and intuitive experience.  
- Updated the victim direction indicator to provide clearer visual feedback on the victim's position relative to the drone.  
- Improved performance of UI updates during keyboard control.  
- Updated status messages to reflect the new control capabilities.  
- Enhanced layout and readability of the Help tab content.  
- Refined color scheme for better visibility in various lighting conditions.

### Fixed
- Resolved issues with control status not updating correctly.  
- Fixed potential UI freezes during rapid input events.  
- Improved error handling for joystick input integration.  
- Addressed memory leaks in long-running simulation sessions.  
- Corrected inconsistencies in status reporting during dataset collection.

### Performance
- Optimized event handling for smoother keyboard and joystick interactions, reducing input lag.  
- Implemented complex logging mechanisms to track user interactions and system performance, aiding in debugging and analysis.  
- Enhanced memory management during UI updates, resulting in a decreased memory footprint and improved responsiveness.  
- Streamlined background processes to minimize CPU usage during idle times, ensuring a more efficient application performance.  
- Improved rendering performance for dynamic UI elements, leading to a smoother user experience during rapid input events.  
- Reduced startup time by code optimization and resource loading improvements.

---

## [V.1.1.1] - Galactic Explorer - 2025-05-09

### Added
**- Added custom dataset directory selection functionality:**  
- New interface in Dataset tab to select output locations  
- Real-time directory path updates in the UI  
- Integration with existing dataset capture system

### Changed
**- Completely redesigned modern user interface:**  
- Enhanced color scheme with a modern dark theme and accent colors  
- Redesigned buttons and controls with consistent styling  
- Added visual feedback for user interactions  
- Enhanced scrolling behavior in configuration panels  
- Modernized progress indicators with color-coded status  
- Canvas-based radar displays victim direction with new indication mechanism

**- Enhanced Config tab with scrollable form:**  
- All config FIELDS rendered dynamically with consistent styling  
- Live updates using config/updated events  
- Form validation with visual feedback  
- Save/load configuration functionality

**- Improved scene creation feedback:**  
- Real-time progress bar during scene creation  
- Displays category (e.g. Rocks, Trees) and item counts  
- Cancel button allows scene generation to be interrupted safely  
- Fixed fallen tree removal and random respawn logic

### Fixed
- Fixed potential filesystem errors  
- Improved thread safety in UI update operations with `_ui_active` flag  
- Enhanced error handling for background thread operations  
- Corrected potential thread deadlocks in dataset collection process  
- Improved shutdown sequence to prevent UI freezes when closing the application

### Performance
**- Optimized UI performance across all tabs:**  
- Added event-driven UI updates instead of polling-based approach  
- Suspended performance monitoring when switching tabs to reduce CPU usage  
- Decreased memory footprint through better resource management  
- Improved responsiveness when switching between tabs

---

## [V.1.1.0] - Cosmic Navigator - 2025-05-08

### Added
**- Added RC transmitter (joystick) control support:**  
- Implemented `rc_controller.py` using `pygame` in a subprocess (macOS-safe)  
- Mapped joystick axes to drone movement and rotation (pitch, roll, yaw, throttle)  
- Applied deadzone filtering and sensitivity scaling (especially yaw and throttle)

**- Added GUI control mode selection at startup:**  
- Tkinter popup lets user choose between Keyboard and RC Controller  
- Seamlessly integrated into simulation launch sequence

**- Implemented multiprocessing-safe communication between RC controller and simulation loop**  
**- Integrated joystick input into event system using `keyboard/move` and `keyboard/rotate` events**

### Changed
- Refactored `main.py` to support dynamic control mode selection and conditional process handling  
- Updated `drone_keyboard_mapper.py`:  
  - Removed use of `reset_controls()` in favor of event-based motion stopping  
  - Corrected yaw direction to match standard RC control convention  
- Updated `drone_movement_transformer.py` to ensure proper `/target` updates even when input is zero  
- Enhanced `keyboard_manager.py` with timeout-based key release detection for better macOS compatibility

### Fixed
- Ensured `DroneControlManager` is always initialized, regardless of input method  
- Fixed issue where drone would continue moving after releasing keys or stick due to missing stop events

### Internal
- All related commits tagged as part of `v1.1.0: adds RC controller support and control mode selection`

---

## [V.1.0.1] - Stellar Fix - 2025-05-08

### Added
- Added dynamically moving objects such as birds and falling trees:  
  - Option to select number of dynamic objects  
- Enhanced simulation performance for dynamic objects

---

## [V.1.0.0] - Stellar Fix - 2025-05-05

### Added
**- Added Status tab with comprehensive victim detection visualization:**  
- Direction indicator with radar-like display showing victim's position accurately relative to drone's heading  
- Elevation indicator displaying victim's height difference in meters with color coding  
- Distance display with color coding (green=near, orange=medium, red=far)  
- Signal strength indicator that increases as drone gets closer to victim

**- Enhanced error handling for object existence checking with new `does_object_exist_by_alias()` function**  
**- Added event subscription system for real-time victim position tracking**  
**- Added complete `scene_manager.py` implementation with fully event-driven scene creation**  
**- Added visual feedback when configuration settings are modified**  
**- Added safety distance check to ensure victim spawns at least 2m away from drone's starting position**  
**- Added category-based scene organization with proper parent-child relationships**

### Changed
**- Completely refactored scene creation system:**  
- Removed progressive/threaded creation in favor of event-based architecture  
- Implemented batch processing to maintain UI responsiveness

**- Enhanced configuration system:**  
- Improved config saving/loading with proper UI synchronization  
- Added `_on_config_updated_gui` method to handle external config changes  
- Implemented visual highlights to show when settings are modified

**- Modified floor creation to ensure it updates size when `area_size` configuration changes**  
**- Improved UI responsiveness using Tkinter's `after()` method for safer UI updates**  
**- Enhanced `SimConnection` shutdown process to safely handle event-triggered shutdowns**  
**- Updated `depth_dataset_collector` to properly emit victim vector data for position tracking**  
**- Extended event system with more topics and improved handling**  
**- Implemented proper coordinate transformation to align victim indicator with drone's orientation**

### Fixed
- Fixed configuration not saving/loading properly with direct UI synchronization  
- Fixed floor not resizing when `area_size` is changed in configuration  
- Fixed potential UI freezing during updates by properly scheduling UI operations  
- Improved error handling in victim direction calculation  
- Corrected coordinate transformation in `get_victim_direction()` to show accurate victim positions  
- Fixed circular reference issues in scene hierarchy with improved category naming

### Removed
**- Removed multiple redundant scene creation files:**  
- `scene_core.py`  
- `scene_creator_base.py`  
- `scene_progressive.py`  
- `scene_pos_sampler.py`  
- `scene_object_creators.py`  
**- Eliminated progressive scene creation in favor of more efficient event-based approach**

---

## [V.0.10.0] - Quantum Leap - 2025-05-03

### Added
- Event-driven depth dataset collection via `simulation/frame` events  
- New config `victim_detection_threshold` to fire `victim/detected` alarms  
- Immediate one-off capture when victim detected (bypasses frame skip)  
- Thread-safe event publishes from background threads (save and capture events)  
- Automatic unsubscribe from all dataset events on `shutdown()` to avoid leaks  
- Implemented singleton pattern for core managers (EventManager, KeyboardManager, SimConnection)  
- Added `SceneCreatorBase` abstract class to standardize scene creation approaches  
- Created new `scene_helpers.py` module with helper functions for scene creation  
- Added `setup_scene_event_handlers()` for event-based scene management  
- Added `create_terrain_object()` helper function to standardize terrain object creation

### Changed
- Replaced dummy distances with real Euclidean distance calculations  
- Configurable sampling rate via `dataset_capture_frequency`  
- Introduced capture and batch events: `dataset/capture/complete`, `dataset/batch/saved`, `dataset/batch/error`  
- Refactored Controls subsystem to use singleton pattern  
- Converted all direct sim references to use SimConnection singleton  
- Moved from threaded simulation architecture to single-thread event-driven approach  
- Reimplemented core scene creation functionality using the new `SceneCreatorBase` structure  
- Enhanced victim direction vector error handling in `depth_dataset_collector.py`  
- Refactored all menu classes to use the `EventManager` singleton  
- Improved `main.py` to explicitly calculate `delta_time` between simulation frames  
- Simplified object creation workflow with normalized property setting

### Fixed
- Proper cleanup of event subscriptions on shutdown  
- Fixed Cancel Creating Environment button being disabled during scene creation  
- Improved error handling in victim direction vectors in `depth_dataset_collector.py`  
- Consolidated terrain element creation in `create_terrain_object` helper function  
- Fixed simulation termination and shutdown sequence  
- Fixed scene creation cancellation issues

### Removed
- Eliminated `physics_utils.py` in favor of direct property setting via SimConnection  
- Removed `sim_utils.py` as it's no longer needed with the new architecture  
- Removed global creator reference in `scene_progressive.py` in favor of module attribute  
- Eliminated the need to pass sim and event_manager instances throughout the codebase

---

## [V.0.9.0] - Celestial Odyssey - 2025-05-02

### Added
**- New teleportation logic for the quadcopter:**
  - Introduced `teleport_quadcopter_to_edge()` function in `scene_progressive.py` to avoid physics optimization.
**- Event-driven scene creation:**
  - Implemented architecture with dedicated event topics for streamlined scene generation.
**- Completion tracking:**
  - Added completion state handling to `ProgressiveSceneCreator`.
**- Project documentation:**
  - Created `CHANGELOG.md` to track project changes.

### Changed
- Moved quadcopter teleportation to the beginning of scene creation to prevent physics issues.
- Improved property checking in `physics_utils.py` to verify support before applying settings.
- Removed `scene_manager.py` as a redundant abstraction layer.
- Updated all direct imports referencing removed modules.
- Refactored teleportation logic to eliminate duplication across modules.
- Renamed `create_scene_threaded` to `create_scene_queued` for clarity.

### Fixed
- Fixed "property is unknown" error in `physics_utils.py`.
- Prevented simulation startup bug caused by repeated teleportation and physics reinitialization.
- Resolved `ModuleNotFoundError` caused by outdated imports.
- Fixed duplicated logic in quadcopter teleportation routines.
- Corrected misleading function name and modular responsibilities.

### Removed
- Deleted `scene_manager.py` as it was no longer necessary.
- Removed global `_active_creator` from `scene_progressive.py` in favor of event-based communication.

---

## [V.0.6.0] - Galactic Frontier - 2025-04-28

_(Note: No changelog entries were documented for this release.)_

---

## [V.0.1.0] - Nebula - 2025-04-20

### Added
**- Initial release of the Disaster Simulation CoppeliaSim project:**
  - Basic scene with single rectangle object generation.
  - Quadcopter model integration with basic manual keyboard control.

