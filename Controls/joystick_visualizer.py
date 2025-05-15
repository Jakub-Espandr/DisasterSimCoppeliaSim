import tkinter as tk
import math

class JoystickVisualizer(tk.Canvas):
    def __init__(self, parent, width=200, height=200, **kwargs):
        """
        Creates a visual representation of a joystick position
        
        Parameters:
        - parent: Parent tkinter frame/window
        - width: Canvas width
        - height: Canvas height
        """
        # Set default background to dark gray if not specified
        if "bg" not in kwargs and "background" not in kwargs:
            kwargs["bg"] = "#2E2E2E"
            
        super().__init__(parent, width=width, height=height, **kwargs)
        
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.max_radius = min(self.center_x, self.center_y) - 10
        
        # Draw the base elements
        self._draw_base()
        
        # Initialize stick position at center
        self.x_pos = 0
        self.y_pos = 0
        self.stick = self.create_oval(
            self.center_x - 10, 
            self.center_y - 10, 
            self.center_x + 10, 
            self.center_y + 10, 
            fill="#00AAFF", 
            outline="#FFFFFF"
        )
    
    def _draw_base(self):
        """Draw the base elements of the joystick visualizer"""
        # Draw outer circle (boundary)
        self.create_oval(
            self.center_x - self.max_radius,
            self.center_y - self.max_radius,
            self.center_x + self.max_radius,
            self.center_y + self.max_radius,
            outline="#FFFFFF",
            width=2
        )
        
        # Draw center point
        self.create_oval(
            self.center_x - 3,
            self.center_y - 3,
            self.center_x + 3,
            self.center_y + 3,
            fill="#FFFFFF",
            outline=""
        )
        
        # Draw crosshairs
        self.create_line(
            self.center_x - self.max_radius, 
            self.center_y,
            self.center_x + self.max_radius,
            self.center_y,
            fill="#555555",
            dash=(4, 4)
        )
        self.create_line(
            self.center_x,
            self.center_y - self.max_radius,
            self.center_x,
            self.center_y + self.max_radius,
            fill="#555555",
            dash=(4, 4)
        )
        
        # Add labels for directions
        self.create_text(
            self.center_x, 
            self.center_y - self.max_radius + 10,
            text="Forward/Up",
            fill="#AAAAAA",
            font=("Segoe UI", 8)
        )
        
        self.create_text(
            self.center_x, 
            self.center_y + self.max_radius - 10,
            text="Back/Down",
            fill="#AAAAAA",
            font=("Segoe UI", 8)
        )
        
        self.create_text(
            self.center_x - self.max_radius + 10, 
            self.center_y,
            text="Left",
            fill="#AAAAAA",
            font=("Segoe UI", 8),
            angle=90
        )
        
        self.create_text(
            self.center_x + self.max_radius - 10, 
            self.center_y,
            text="Right",
            fill="#AAAAAA",
            font=("Segoe UI", 8),
            angle=270
        )
    
    def update_position(self, x, y):
        """
        Update the joystick position
        
        Parameters:
        - x: X position (-1.0 to 1.0)
        - y: Y position (-1.0 to 1.0)
        """
        # Store the position
        self.x_pos = x
        self.y_pos = y
        
        # Calculate pixel position (invert Y axis so up is negative)
        pixel_x = self.center_x + int(x * self.max_radius)
        pixel_y = self.center_y - int(y * self.max_radius)  # Negative because Y is inverted in tkinter
        
        # Update the stick position
        self.coords(
            self.stick,
            pixel_x - 10,
            pixel_y - 10,
            pixel_x + 10,
            pixel_y + 10
        ) 