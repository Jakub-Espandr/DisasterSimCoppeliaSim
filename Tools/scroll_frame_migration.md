# Migrating to ScrollFrame - v1.4.0

This document provides guidelines for migrating existing scrollable frames in the application to use the new `ScrollFrame` class introduced in v1.4.0.

## Benefits of Using ScrollFrame

- **Cross-platform scrolling**: Optimized for macOS, Windows, and Linux
- **Trackpad gesture support**: Enhanced support for trackpad gestures with natural scrolling
- **Drag-to-scroll**: Added ability to click and drag to scroll content
- **Consistent behavior**: Standardized scrolling behavior throughout the application
- **Programmatic control**: Methods for controlling scroll position programmatically
- **Configurable options**: Various options to customize scrolling behavior

## Migration Steps

### Step 1: Import the ScrollFrame Class

Add the following import to your file:

```python
from Tools.scroll_frame import ScrollFrame
```

### Step 2: Replace Existing Scrollable Canvas Code

Find code that looks like this:

```python
# Create a canvas with scrollbar for the content
canvas = tk.Canvas(parent, bg="#0a0a0a", highlightthickness=0)
scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

# Configure the canvas
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Create a window in the canvas to hold the scrollable frame
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the scrollbar and canvas
scrollbar.pack(side="right", fill="y", padx=(5, 0))
canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))

# Add mouse wheel scrolling support
canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))

# Update canvas width when window is resized
def on_resize(event):
    canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
canvas.bind('<Configure>', on_resize)
```

And replace it with:

```python
# Create a ScrollFrame instance
scroll_frame = ScrollFrame(parent, bg="#0a0a0a")
scroll_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

# Use scrollable_frame as the container for your content
scrollable_frame = scroll_frame.scrollable_frame
```

### Step 3: Update Content Placement

Make sure all your content is added to `scrollable_frame` (the same way you did before):

```python
# Example: Adding content to the scrollable frame
label = ttk.Label(scrollable_frame, text="Content title")
label.pack(fill="x", pady=10)
```

### Step 4: Use Additional Features (Optional)

Take advantage of new methods for programmatic control:

```python
# Scroll to the top
scroll_frame.scroll_to_top()

# Scroll to the bottom
scroll_frame.scroll_to_bottom()

# Scroll to a specific position (0.0 to 1.0)
scroll_frame.scroll_to_position(0.5)  # Scroll to middle
```

## Example: Before and After

### Before (v1.3.3 and earlier)

```python
def _build_config_tab(self, parent):
    # Create a canvas with scrollbar for the config options
    canvas = tk.Canvas(parent, bg="#0a0a0a", highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Configure the canvas
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    # Create a window in the canvas to hold the scrollable frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack the scrollbar and canvas with padding
    scrollbar.pack(side="right", fill="y", padx=(5, 0))
    canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
    
    # Title
    ttk.Label(scrollable_frame, text="Configuration", style="Title.TLabel").pack(pady=(0,20))
    
    # Add mouse wheel scrolling support
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
    canvas.bind_all("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))
    
    # Update canvas width when window is resized
    def on_resize(event):
        canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
    canvas.bind('<Configure>', on_resize)
    
    # Add content here...
```

### After (v1.4.0)

```python
def _build_config_tab(self, parent):
    # Create a ScrollFrame instance
    scroll_frame = ScrollFrame(parent, bg="#0a0a0a")
    scroll_frame.pack(fill="both", expand=True)
    
    # Get the scrollable frame to add content to
    scrollable_frame = scroll_frame.scrollable_frame
    
    # Title
    ttk.Label(scrollable_frame, text="Configuration", style="Title.TLabel").pack(pady=(0,20))
    
    # Add content here...
```

## Advanced Configuration Options

The `ScrollFrame` class accepts several configuration options:

```python
scroll_frame = ScrollFrame(
    parent,
    bg="#0a0a0a",                 # Background color
    scrollbar_width=12,           # Width of the scrollbar
    scrollbar_side="right",       # Side to place the scrollbar ("right" or "left")
    hide_scrollbar=False,         # Whether to hide scrollbar when not needed
    padding=0,                    # Padding around the content
    smooth_scroll=True            # Whether to use smooth scrolling for trackpad gestures
)
```

## Important Notes

1. Each tab or panel should use its own `ScrollFrame` instance.
2. Never use `bind_all` for wheel events if you're using `ScrollFrame` as it's handled internally.
3. The `ScrollFrame` class handles all resize events automatically.
4. See `Tools/scroll_frame_demo.py` for a complete demonstration of all features.

## Getting Help

If you encounter any issues during migration, please refer to the demo application in `Tools/scroll_frame_demo.py` for examples of all supported features and configurations. 