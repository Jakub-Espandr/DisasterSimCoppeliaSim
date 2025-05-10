from PIL import Image, ImageDraw
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def create_app_icon(custom_image_path=None):
    """
    Create application icons from either a custom image or generate a default one.
    
    Args:
        custom_image_path (str, optional): Path to your custom image file. 
                                         If provided, this image will be used as the base for the icons.
                                         Supported formats: PNG, JPG, ICO
    """
    if custom_image_path and os.path.exists(custom_image_path):
        print(f"Using custom image: {custom_image_path}")
        try:
            # Load and resize the custom image
            image = Image.open(custom_image_path)
            # Convert to RGBA if not already
            image = image.convert('RGBA')
            # Resize to 256x256
            image = image.resize((256, 256), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return False
    else:
        print("No custom image provided or file not found. Creating default icon...")
        # Create a 256x256 image with a dark background
        size = 256
        image = Image.new('RGBA', (size, size), (26, 26, 26, 255))
        draw = ImageDraw.Draw(image)
        
        # Draw a circle
        circle_color = (0, 180, 216, 255)  # Modern blue accent color
        circle_radius = size * 0.4
        circle_center = (size/2, size/2)
        draw.ellipse(
            (circle_center[0] - circle_radius, 
             circle_center[1] - circle_radius,
             circle_center[0] + circle_radius, 
             circle_center[1] + circle_radius),
            fill=circle_color
        )
        
        # Draw a drone symbol (simplified)
        drone_color = (255, 255, 255, 255)  # White
        drone_size = size * 0.3
        drone_center = (size/2, size/2)
        
        # Draw drone body
        draw.rectangle(
            (drone_center[0] - drone_size/2,
             drone_center[1] - drone_size/4,
             drone_center[0] + drone_size/2,
             drone_center[1] + drone_size/4),
            fill=drone_color
        )
        
        # Draw drone arms
        arm_length = drone_size * 0.6
        arm_width = drone_size * 0.1
        
        # Horizontal arms
        draw.rectangle(
            (drone_center[0] - arm_length/2,
             drone_center[1] - arm_width/2,
             drone_center[0] + arm_length/2,
             drone_center[1] + arm_width/2),
            fill=drone_color
        )
        
        # Vertical arms
        draw.rectangle(
            (drone_center[0] - arm_width/2,
             drone_center[1] - arm_length/2,
             drone_center[0] + arm_width/2,
             drone_center[1] + arm_length/2),
            fill=drone_color
        )
    
    try:
        # Create assets directory if it doesn't exist
        if not os.path.exists('assets'):
            os.makedirs('assets')
        
        # Save as ICO file with multiple sizes
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        image.save('assets/icon.ico', format='ICO', sizes=icon_sizes)
        
        # Save as PNG with specific settings for macOS
        png_image = image.copy()
        png_image.save('assets/icon.png', format='PNG', optimize=True)
        
        # Create a smaller version for macOS dock
        small_size = 128
        small_image = image.resize((small_size, small_size), Image.Resampling.LANCZOS)
        small_image.save('assets/icon_small.png', format='PNG', optimize=True)
        
        print("Icon files created successfully!")
        print(f"ICO file: {os.path.abspath('assets/icon.ico')}")
        print(f"PNG file: {os.path.abspath('assets/icon.png')}")
        print(f"Small PNG file: {os.path.abspath('assets/icon_small.png')}")
        return True
    except Exception as e:
        print(f"Error saving icon files: {str(e)}")
        return False

def select_and_create_icon():
    """Open a file dialog to select an image and create icons from it"""
    # Create a root window but hide it
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Show file dialog
    file_path = filedialog.askopenfilename(
        title="Select Icon Image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.ico"),
            ("All files", "*.*")
        ]
    )
    
    if file_path:
        # Create icons from selected image
        success = create_app_icon(file_path)
        if success:
            messagebox.showinfo("Success", "Icon files created successfully!")
        else:
            messagebox.showerror("Error", "Failed to create icon files. Check console for details.")
    else:
        print("No file selected. Creating default icon...")
        create_app_icon()
    
    # Destroy the root window
    root.destroy()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # If a custom image path is provided as a command-line argument
        create_app_icon(sys.argv[1])
    else:
        # Show file dialog for icon selection
        select_and_create_icon() 