## [V.1.3.0] - HyperDrive Navigator - 2025-05-10

### Added
- Added UI keyboard control capabilities:
  - Direct keyboard input through the application window
  - Control status indicator in Status tab
  - Proper focus handling for seamless control switching
- Added RC joystick controller documentation and support
- Added comprehensive application icon support:
  - Platform-specific icon loading for macOS and Windows
  - Error handling for missing icon files
  - Resolution-appropriate icon rendering
- Added tools for showing datasets, enhancing data visualization and analysis capabilities:
  - Preview pane for captured depth images
  - Basic preprocessing tools
  - Quick-access export functionality
- Enhanced Help tab with expanded information and improved organization.

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

## [V.1.1.1] - Galactic Explorer - 2025-05-09

### Added
- Added custom dataset directory selection functionality:
  - New interface in Dataset tab to select output locations 
  - Real-time directory path updates in the UI
  - Integration with existing dataset capture system

### Changed
- Completely redesigned modern user interface:
  - Enhanced color scheme with a modern dark theme and accent colors
  - Redesigned buttons and controls with consistent styling
  - Added visual feedback for user interactions
  - Enhanced scrolling behavior in configuration panels
  - Modernized progress indicators with color-coded status
  - Canvas-based radar displays victim direction with new indication mechanism
- Enhanced Config tab with scrollable form:
  - All config FIELDS rendered dynamically with consistent styling
  - Live updates using config/updated events
  - Form validation with visual feedback
  - Save/load configuration functionality
- Improved scene creation feedback:
  - Real-time progress bar during scene creation
  - Displays category (e.g. Rocks, Trees) and item counts
  - Cancel button allows scene generation to be interrupted safely
  - Fixed fallen tree removal and random respawn logic

### Fixed
- Fixed potential filesystem errors
- Improved thread safety in UI update operations with _ui_active flag
- Enhanced error handling for background thread operations
- Corrected potential thread deadlocks in dataset collection process
- Improved shutdown sequence to prevent UI freezes when closing the application

### Performance
- Optimized UI performance across all tabs:
  - Added event-driven UI updates instead of polling-based approach
  - Suspended performance monitoring when switching tabs to reduce CPU usage
- Decreased memory footprint through better resource management
- Improved responsiveness when switching between tabs

## [V.1.1.0] - Cosmic Navigator - 2025-05-08

### Added
- Added RC transmitter (joystick) control support:
  - Implemented `rc_controller.py` using `pygame` in a subprocess (macOS-safe)
  - Mapped joystick axes to drone movement and rotation (pitch, roll, yaw, throttle)
  - Applied deadzone filtering and sensitivity scaling (especially yaw and throttle)
- Added GUI control mode selection at startup:
  - Tkinter popup lets user choose between Keyboard and RC Controller
  - Seamlessly integrated into simulation launch sequence
- Implemented multiprocessing-safe communication between RC controller and simulation loop
- Integrated joystick input into event system using `keyboard/move` and `keyboard/rotate` events

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


## [V.1.0.1] - Stellar Fix - 2025-05-08

### Added
- Added Dynamiclly moving objects such as birds and falling trees:
  - Option to select number of dynamic objects
- Enhanced simulation performance for dynamic objects

## [V.1.0.0] - Stellar Fix - 2025-05-05

### Added
- Added Status tab with comprehensive victim detection visualization:
  - Direction indicator with radar-like display showing victim's position accurately relative to drone's heading
  - Elevation indicator displaying victim's height difference in meters with color coding
  - Distance display with color coding (green=near, orange=medium, red=far)
  - Signal strength indicator that increases as drone gets closer to victim
- Enhanced error handling for object existence checking with new `does_object_exist_by_alias()` function
- Added event subscription system for real-time victim position tracking
- Added complete scene_manager.py implementation with fully event-driven scene creation
- Added visual feedback when configuration settings are modified
- Added safety distance check to ensure victim spawns at least 2m away from drone's starting position
- Added category-based scene organization with proper parent-child relationships

### Changed
- Completely refactored scene creation system:
  - Removed progressive/threaded creation in favor of event-based architecture
  - Implemented batch processing to maintain UI responsiveness
- Enhanced configuration system:
  - Improved config saving/loading with proper UI synchronization
  - Added `_on_config_updated_gui` method to handle external config changes
  - Implemented visual highlights to show when settings are modified
- Modified floor creation to ensure it updates size when area_size configuration changes
- Improved UI responsiveness using Tkinter's `after()` method for safer UI updates
- Enhanced SimConnection shutdown process to safely handle event-triggered shutdowns
- Updated depth_dataset_collector to properly emit victim vector data for position tracking
- Extended event system with more topics and improved handling
- Implemented proper coordinate transformation to align victim indicator with drone's orientation

### Fixed
- Fixed configuration not saving/loading properly with direct UI synchronization
- Fixed floor not resizing when area_size is changed in configuration
- Fixed potential UI freezing during updates by properly scheduling UI operations
- Improved error handling in victim direction calculation
- Corrected coordinate transformation in get_victim_direction() to show accurate victim positions
- Fixed circular reference issues in scene hierarchy with improved category naming

### Removed
- Removed multiple redundant scene creation files:
  - scene_core.py
  - scene_creator_base.py
  - scene_progressive.py
  - scene_pos_sampler.py
  - scene_object_creators.py
- Eliminated progressive scene creation in favor of more efficient event-based approach

## [V.0.10.0] - Quantum Leap - 2025-05-03

### Added
- Event-driven depth dataset collection via `simulation/frame` events
- New config `victim_detection_threshold` to fire `victim/detected` alarms
- Immediate one-off capture when victim detected (bypasses frame skip)
- Thread-safe event publishes from background threads (save and capture events)
- Automatic unsubscribe from all dataset events on `shutdown()` to avoid leaks
- Created TODO.md file to track planned features and improvements
- Implemented singleton pattern for core managers (EventManager, KeyboardManager, SimConnection)
- Added SceneCreatorBase abstract class to standardize scene creation approaches
- Created new scene_helpers.py module with helper functions for scene creation
- Added setup_scene_event_handlers() for event-based scene management
- Added create_terrain_object() helper function to standardize terrain object creation

### Changed
- Replaced dummy distances with real Euclidean distance calculations
- Configurable sampling rate via `dataset_capture_frequency`
- Introduced capture and batch events: `dataset/capture/complete`, `dataset/batch/saved`, `dataset/batch/error`
- Refactored Controls subsystem to use singleton pattern
- Converted all direct sim references to use SimConnection singleton
- Created scene_helpers.py with utility functions to reduce code duplication
- Moved from threaded simulation architecture to single-thread event-driven approach
- Reimplemented core scene creation functionality using the new SceneCreatorBase structure
- Enhanced victim direction vector error handling in depth_dataset_collector.py
- Refactored all menu classes to use the EventManager singleton
- Improved main.py to explicitly calculate delta_time between simulation frames
- Simplified object creation workflow with normalized property setting

### Fixed
- Proper cleanup of event subscriptions on shutdown
- Fixed Cancel Creating Environment button being disabled during scene creation
- Improved error handling in victim direction vectors in depth_dataset_collector.py
- Consolidated terrain element creation in create_terrain_object helper function
- Fixed simulation termination and shutdown sequence
- Fixed scene creation cancellation issues

### Removed
- Eliminated physics_utils.py in favor of direct property setting via SimConnection
- Removed sim_utils.py as it's no longer needed with the new architecture
- Removed global creator reference in scene_progressive.py in favor of module attribute
- Eliminated the need to pass sim and event_manager instances throughout the codebase

## [V.0.9.0] - Celestial Odyssey - 2025-05-02

### Added
- New `teleport_quadcopter_to_edge()` function in scene_progressive.py that doesn't trigger physics optimization
- Created CHANGELOG.md to track project changes
- Added proper completion state tracking to ProgressiveSceneCreator
- Implemented event-driven scene creation architecture with dedicated event topics

### Fixed
- Fixed "property is unknown" error in physics_utils.py by using correct property names
- Fixed issue with physics optimization being triggered multiple times when teleporting the quadcopter
- Fixed ModuleNotFoundError after removing scene_manager.py by updating imports in dependent files
- Fixed bug causing repeated teleportation and physics optimization messages by adding proper completion state tracking
- Fixed code duplication in quadcopter teleportation by centralizing the functionality in a single function
- Fixed misleading function name by renaming `create_scene_threaded` to `create_scene_queued` to better reflect its actual behavior

### Changed
- Moved quadcopter teleportation to the beginning of scene creation process to prevent physics issues
- Improved property checking in physics_utils.py to verify support before attempting to set properties
- Removed unnecessary scene_manager.py facade to simplify the codebase
- Updated direct imports in main.py, depth_dataset_collector.py, and main_menu.py to reference source modules
- Updated copilot-agent-instructions.md with guidance for maintaining the changelog
- Modified scene creation update mechanism to respect completion state
- Refactored scene creation to use event system instead of global variables
- Enhanced create_scene and create_scene_threaded to publish events when event_manager is provided
- Refactored quadcopter teleportation code to eliminate duplication between scene_core.py and scene_progressive.py
- Renamed `create_scene_threaded` to `create_scene_queued` to better reflect its actual functionality

### Removed
- Deleted scene_manager.py facade module as it was redundant
- Removed global _active_creator variable in scene_progressive.py in favor of event-based communication

## [V.0.6.0] - Galactic Frontier - 2025-04-28

## [V.0.1.0] - Nebula - 2025-04-27