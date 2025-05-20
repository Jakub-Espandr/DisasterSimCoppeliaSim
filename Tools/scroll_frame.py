import tkinter as tk
from tkinter import ttk
import platform
import sys
import time

class ScrollFrame(ttk.Frame):
    """
    A scrollable frame that supports both trackpad gestures and traditional scrollbar
    with improved cross-platform compatibility.
    
    Features:
    - Smooth trackpad scrolling with gesture support
    - Traditional scrollbar that works alongside trackpad scrolling
    - Cross-platform compatibility for different OS scrolling behaviors
    - Drag-to-scroll capability
    - Automatic scrollbar visibility management
    """
    
    def __init__(self, parent, *args, **kwargs):
        """
        Initialize a new ScrollFrame.
        
        Args:
            parent: The parent widget
            *args, **kwargs: Additional arguments passed to the Frame constructor
            
        Keyword Args:
            bg (str): Background color for the canvas. Defaults to "#0a0a0a".
            scrollbar_width (int): Width of the scrollbar. Defaults to 12.
            scrollbar_side (str): Side to place the scrollbar ("right" or "left"). Defaults to "right".
            hide_scrollbar (bool): Whether to hide the scrollbar when not needed. Defaults to False.
            padding (int): Padding around the internal frame. Defaults to 0.
            smooth_scroll (bool): Whether to use smooth scrolling for trackpad gestures. Defaults to True.
        """
        # Extract bg and other options before initializing ttk.Frame
        bg_color = kwargs.pop("bg", "#0a0a0a") if "bg" in kwargs else "#0a0a0a"
        scrollbar_width = kwargs.pop("scrollbar_width", 12)
        scrollbar_side = kwargs.pop("scrollbar_side", "right")
        self.hide_scrollbar = kwargs.pop("hide_scrollbar", False)
        padding = kwargs.pop("padding", 0)
        self.smooth_scroll = kwargs.pop("smooth_scroll", True)
        
        # Initialize ttk.Frame without bg parameter
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        
        # Set platform-specific scroll factors first
        self._configure_scroll_factors()
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create the scrollable frame inside the canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Position with internal padding using the canvas coordinates
        x_padding = padding
        y_padding = padding
        self.scrollable_window = self.canvas.create_window(
            (x_padding, y_padding), 
            window=self.scrollable_frame, 
            anchor="nw",
            tags="frame"
        )
        
        # Configure the canvas scrolling behavior
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack the scrollbar and canvas
        if scrollbar_side == "right":
            self.scrollbar.pack(side="right", fill="y")
            self.canvas.pack(side="left", fill="both", expand=True)
        else:
            self.scrollbar.pack(side="left", fill="y")
            self.canvas.pack(side="right", fill="both", expand=True)
        
        # Initialize variables for two-finger scrolling (added here to avoid errors)
        self._last_press_time = 0
        self._last_motion_pos = None
        
        # Bind events for scrolling and resizing
        self._bind_events()
    
    def _bind_events(self):
        """Bind all necessary events for scrolling and resizing."""
        # Update the scrollregion when the size of the scrollable frame changes
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self._on_frame_configure()
        )
        
        # Handle resize of the canvas
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Bind mouse wheel events for scrolling (platform-specific)
        self._bind_mouse_scroll()
        
        # Add drag to scroll capability
        self._bind_drag_scroll()
        
        # Add focus events for better trackpad gesture capture on macOS
        if self.os_name == "Darwin":
            self.canvas.bind("<Enter>", self._on_mouse_enter)
            self.canvas.bind("<Leave>", self._on_mouse_leave)
    
    def _configure_scroll_factors(self):
        """Configure platform-specific scroll factors and behaviors."""
        self.os_name = platform.system()
        
        # Set suitable defaults for each platform
        if self.os_name == "Darwin":  # macOS
            self.scroll_factor = 0.2  # Reduced scrolling speed for macOS trackpads (was 0.5)
            self.natural_scroll = True  # Use natural scrolling on macOS
        elif self.os_name == "Windows":
            self.scroll_factor = 1.0  # Default for Windows
            self.natural_scroll = False  # Standard scrolling on Windows
        else:  # Linux and others
            self.scroll_factor = 1.0  # Default for other platforms
            self.natural_scroll = False  # Standard scrolling on Linux
    
    def _bind_mouse_scroll(self):
        """Bind mouse wheel events with platform-specific handling."""
        # Unbind any previously bound scroll events
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
        
        # Standard mouse wheel for Windows and macOS
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # For Linux
        self.canvas.bind("<Button-4>", self._on_linux_scroll)
        self.canvas.bind("<Button-5>", self._on_linux_scroll)
        
        # For macOS specific events (additional bindings that might help with trackpad)
        if self.os_name == "Darwin":
            # Bind mouse wheel event globally to capture trackpad gestures
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
            
            # Bind the standard mouse button 2 (middle button, often mapped to trackpad gestures)
            self.canvas.bind("<Button-2>", self._on_trackpad_motion)
            self.bind_all("<Button-2>", self._on_trackpad_motion, add="+")
            
            # Bind to key + scroll combinations which are sometimes used for gestures
            self.canvas.bind_all("<Shift-MouseWheel>", self._on_mousewheel, add="+")
            self.canvas.bind_all("<Control-MouseWheel>", self._on_mousewheel, add="+")
            
            # For two-finger scrolling, also try B2-Motion events
            self.canvas.bind("<B2-Motion>", self._on_two_finger_scroll)
            self.canvas.bind_all("<B2-Motion>", self._on_two_finger_scroll, add="+")
            
            # Bind button press and motion for tracking two-finger scrolling
            self.canvas.bind("<ButtonPress>", self._on_button_press)
            self.canvas.bind("<Motion>", self._on_motion)
        else:
            # For touch gestures on other platforms
            if hasattr(self.canvas, "bind_all"):
                self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
                self.canvas.bind_all("<Button-4>", self._on_linux_scroll)
                self.canvas.bind_all("<Button-5>", self._on_linux_scroll)
    
    def _bind_drag_scroll(self):
        """Bind events for drag-to-scroll capability."""
        self.canvas.bind("<ButtonPress-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self._on_drag_end)
        self._drag_data = {"y": 0, "dragging": False}
    
    def _on_frame_configure(self):
        """Update the scrollregion when the frame size changes."""
        # Get the current bbox of all items
        bbox = self.canvas.bbox("all")
        if bbox:
            # Create scrollregion slightly larger to account for any padding
            x1, y1, x2, y2 = bbox
            self.canvas.configure(scrollregion=bbox)
        
        # Hide or show scrollbar based on content size
        if self.hide_scrollbar:
            scroll_needed = (self.scrollable_frame.winfo_reqheight() > self.canvas.winfo_height())
            if scroll_needed and not self.scrollbar.winfo_viewable():
                self.scrollbar.pack(side="right", fill="y", before=self.canvas)
            elif not scroll_needed and self.scrollbar.winfo_viewable():
                self.scrollbar.pack_forget()
    
    def _on_canvas_configure(self, event):
        """Adjust the internal frame width when the canvas is resized."""
        # Update the width of the frame to match the canvas
        self.canvas.itemconfig(self.scrollable_window, width=event.width)
        
        # Check if scrollbar is needed after resize
        self._on_frame_configure()
    
    def _on_mousewheel(self, event):
        """Handle the mouse wheel event with platform-specific behavior."""
        try:
            if self.os_name == "Darwin":
                # macOS: handle trackpad gestures differently
                # on macOS, event.delta can be much smaller for trackpad gestures
                delta = event.delta
                
                # For very small deltas (typical of trackpad gestures), amplify slightly
                if abs(delta) < 5:
                    delta = delta * 3  # Amplify small movements from trackpad
            else:
                # Windows: normalize the delta
                delta = event.delta // 120
            
            # Apply natural scrolling if enabled (invert direction)
            if self.natural_scroll:
                delta = -delta
            
            # Apply scroll factor to adjust speed
            delta = delta * self.scroll_factor
            
            # Debugging: log the delta value to help diagnose issues
            # print(f"Scroll delta: {delta} (original: {event.delta})")
            
            # Perform the scroll - different approach for macOS for smoother feeling
            if self.os_name == "Darwin" and self.smooth_scroll:
                # Always use smooth scrolling for macOS trackpad
                self._smooth_scroll(delta)
            else:
                # For other platforms, or if smooth scrolling is disabled
                self.canvas.yview_scroll(-int(delta), "units")
        except Exception as e:
            print(f"Mousewheel error: {e}")
    
    def _on_linux_scroll(self, event):
        """Handle scroll events on Linux."""
        if event.num == 4:  # Scroll up
            delta = 1
        else:  # event.num == 5, scroll down
            delta = -1
        
        # Apply natural scrolling if enabled
        if self.natural_scroll:
            delta = -delta
            
        # Apply scroll factor
        delta = delta * self.scroll_factor
        
        # Perform the scroll
        if self.smooth_scroll:
            self._smooth_scroll(delta)
        else:
            self.canvas.yview_scroll(-int(delta), "units")
    
    def _smooth_scroll(self, delta):
        """Implement smooth scrolling with small increments."""
        # For small movements, break it into smaller steps for smoothness
        if self.os_name == "Darwin":
            # Use more steps for macOS for smoother trackpad experience
            steps = 8
        else:
            steps = 5
            
        increment = delta / steps
        
        def _step(remaining):
            if remaining > 0:
                self.canvas.yview_scroll(-int(increment), "units")
                self.after(5 if self.os_name == "Darwin" else 10, lambda: _step(remaining - 1))
        
        _step(steps)
    
    def _on_drag_start(self, event):
        """Start the drag-to-scroll operation."""
        # Only initiate drag scroll if we're not on a widget that needs click events
        if isinstance(event.widget, (tk.Text, tk.Entry, ttk.Entry, ttk.Combobox)):
            return
            
        # Record starting position
        self._drag_data["y"] = event.y
        self._drag_data["dragging"] = True
        self.canvas.config(cursor="fleur")  # Change cursor to indicate dragging
    
    def _on_drag_motion(self, event):
        """Handle mouse motion during drag-to-scroll."""
        if not self._drag_data["dragging"]:
            return
            
        # Calculate distance moved
        delta_y = event.y - self._drag_data["y"]
        
        # Scroll the canvas and update the start position
        if delta_y != 0:
            # Calculate the fraction to move based on canvas height
            fraction = delta_y / self.canvas.winfo_height()
            self.canvas.yview_moveto(self.canvas.yview()[0] - fraction)
            self._drag_data["y"] = event.y
    
    def _on_drag_end(self, event):
        """End the drag-to-scroll operation."""
        self._drag_data["dragging"] = False
        self.canvas.config(cursor="")  # Restore default cursor
    
    def scroll_to_top(self):
        """Scroll to the top of the frame."""
        self.canvas.yview_moveto(0)
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the frame."""
        self.canvas.yview_moveto(1)
    
    def scroll_to_position(self, position):
        """
        Scroll to a specific position in the frame.
        
        Args:
            position (float): Position to scroll to, between 0 (top) and 1 (bottom)
        """
        self.canvas.yview_moveto(position)
    
    def _on_trackpad_motion(self, event):
        """Handle trackpad motion/scroll gestures on macOS."""
        try:
            # Try to extract delta value from event
            # Trackpad events might store delta differently
            if hasattr(event, 'delta'):
                delta = event.delta
            elif hasattr(event, 'y'):
                # Use y position change as delta
                if not hasattr(self, '_last_y'):
                    self._last_y = event.y
                    return
                delta = self._last_y - event.y
                self._last_y = event.y
            else:
                return
                
            # Apply natural scrolling if enabled
            if self.natural_scroll:
                delta = -delta
                
            # Apply scroll factor
            delta = delta * self.scroll_factor
            
            # Always use smooth scrolling for trackpad gestures
            if self.smooth_scroll:
                self._smooth_scroll(delta)
            else:
                self.canvas.yview_scroll(-int(delta), "units")
        except Exception as e:
            print(f"Trackpad motion error: {e}")
    
    def _on_mouse_enter(self, event):
        """Handle mouse entering the canvas area - important for trackpad events."""
        if self.os_name == "Darwin":
            # Take focus when mouse enters to ensure we get trackpad events
            self.canvas.focus_set()
            # Reset any trackpad gesture tracking
            if hasattr(self, '_last_y'):
                del self._last_y
    
    def _on_mouse_leave(self, event):
        """Handle mouse leaving the canvas area."""
        # Nothing special needed here for now, but kept for symmetry
        pass
    
    def _on_button_press(self, event):
        """Track button press to detect potential two-finger scrolling."""
        self._last_press_time = time.time()
        self._last_motion_pos = (event.x, event.y)
    
    def _on_motion(self, event):
        """
        Detect motion that might be two-finger scrolling on macOS.
        Some trackpads send Motion events during two-finger scrolling.
        """
        if self.os_name != "Darwin":
            return
            
        # If we had a recent button press, this might be a click-drag, not a gesture
        current_time = time.time()
        if current_time - self._last_press_time < 0.5:
            return
            
        # Check if we have previous position data to compare with
        if self._last_motion_pos is None:
            self._last_motion_pos = (event.x, event.y)
            return
            
        # Calculate vertical distance moved
        _, last_y = self._last_motion_pos
        delta_y = event.y - last_y
        
        # Only process if significant movement detected (to avoid jitter)
        if abs(delta_y) > 2:
            # Apply natural scrolling concept
            if self.natural_scroll:
                delta_y = -delta_y
                
            # Use smaller factor for this type of event
            delta_y = delta_y * 0.05
            
            # Process the scroll
            if self.smooth_scroll:
                self._smooth_scroll(delta_y)
            else:
                self.canvas.yview_scroll(int(-delta_y), "units")
                
            # Update last position
            self._last_motion_pos = (event.x, event.y)
    
    def _on_two_finger_scroll(self, event):
        """Handle two-finger scrolling events on macOS trackpads."""
        # This is similar to trackpad_motion but specifically for two-finger gesture
        try:
            # Calculate delta based on motion
            if not hasattr(self, '_last_two_finger_y'):
                self._last_two_finger_y = event.y
                return
                
            delta = self._last_two_finger_y - event.y
            self._last_two_finger_y = event.y
            
            # Apply natural scrolling if enabled
            if self.natural_scroll:
                delta = -delta
                
            # Apply scroll factor - use a smaller factor for this type of event
            delta = delta * 0.15
            
            # Smooth scrolling is essential for two-finger gestures
            self._smooth_scroll(delta)
        except Exception as e:
            print(f"Two-finger scroll error: {e}") 