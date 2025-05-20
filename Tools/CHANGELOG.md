# Changelog for View_Depth_Image.py
## [0.4.0] - 2025-05-21
### Added
- New Data Inspector tab for viewing detailed information about depth images, including:
  - Depth image dimensions and statistics (min, max, mean depth).
  - Position (x, y, z) and orientation (roll, pitch, yaw) information.
  - Action labels with human-readable descriptions.
  - Distance measurements to victims and direction vectors.
- Enhanced 3D visualization features, including interactive controls for rotation and perspective switching.
- Color mapping options for depth visualizations, allowing users to select different colormaps.

### Improved
- User interface refinements for a more intuitive experience.
- Enhanced feedback mechanisms for user actions and operations.

### Fixed
- Improved memory management during batch operations to prevent crashes.

--

## [0.3.0] - 2025-05-17
### Added
- Image and 3D depth map visualization with arrow keys.
- Enhanced help tab with comprehensive usage instructions covering all features.

### Improved
- User interface enhancements for better navigation and usability.
- Performance optimizations for loading and displaying large datasets.

--

## [0.2.0] - 2025-05-10
### Added
- Interactive 3D visualization of depth data with multiple viewing angles and color mapping
- Ability to view individual full-size images at orignal resolution with detailed information
- Help tab with comprehensive usage instructions
- Custom dataset directory selection
- Backup system to prevent data loss during operations

### Improved
- User interface with modern styling and consistent color scheme
- Grid display system
- Navigation controls with file selector
- Status messaging system with color-coded feedback

### Fixed
- Image display issues when flipping operations are applied
- Grid layout problems during window resizing
- Memory management for large image datasets

--

## [0.1.0] - 2025-04-27
### Added
- Initial release
- Basic viewing of .npz depth image files
- Simple navigation between files
- Basic flip operations (left-right and up-down)
- Automatic saving of changes 