import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the parent directory to the path so we can import the ScrollFrame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Tools.scroll_frame import ScrollFrame

class ScrollFrameDemo:
    """
    Demo application for the ScrollFrame class, showing different configuration options
    and how to use it in different scenarios.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced ScrollFrame - V1.4.0 Demo")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        
        # Configure the UI
        self._configure_styles()
        self._build_ui()
    
    def _configure_styles(self):
        """Configure ttk styles for the demo."""
        style = ttk.Style()
        
        # Dark theme
        style.configure("TFrame", background="#121212")
        style.configure("TLabelframe", background="#121212")
        style.configure("TLabelframe.Label", background="#121212", foreground="#FFFFFF")
        style.configure("TLabel", background="#121212", foreground="#FFFFFF")
        style.configure("TButton", background="#2a2a2a", foreground="#FFFFFF")
        style.configure("TCheckbutton", background="#121212", foreground="#FFFFFF")
        
        # Title style
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground="#00b4d8")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 12, "bold"), foreground="#c8c8c8")
        
        # Option section styles
        style.configure("Section.TFrame", background="#1a1a1a")
        style.configure("Section.TLabel", background="#1a1a1a", foreground="#FFFFFF")
        
        # Button styles
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"))
    
    def _build_ui(self):
        """Build the user interface."""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top section with title and introduction
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        # Title
        ttk.Label(
            top_frame, 
            text="ScrollFrame Demo - V1.4.0", 
            style="Title.TLabel"
        ).pack(pady=(0, 5))
        
        # Introduction
        intro_text = (
            "This demo showcases the new ScrollFrame class with enhanced trackpad scrolling."
            "\nExplore different scrolling options and features below."
        )
        ttk.Label(
            top_frame, 
            text=intro_text,
            wraplength=800,
            justify="left"
        ).pack(fill="x", pady=(0, 15))
        
        # Create a notebook with tabs for different demos
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create demo tabs
        self._create_basic_demo_tab(notebook)
        self._create_options_demo_tab(notebook)
        self._create_content_demo_tab(notebook)
        self._create_scrolling_methods_tab(notebook)
        
        # Add a status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(
            status_frame,
            text="Enhanced ScrollFrame available in v1.4.0 - Drop-in replacement for scrollable frames",
            foreground="#888888"
        ).pack(side="left")
    
    def _create_basic_demo_tab(self, notebook):
        """Create the basic demo tab with a simple scrollable content."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Basic Demo")
        
        # Add description
        desc_frame = ttk.Frame(tab)
        desc_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(
            desc_frame,
            text="Basic ScrollFrame Example",
            style="Subtitle.TLabel"
        ).pack(anchor="w")
        
        ttk.Label(
            desc_frame,
            text="This is a basic example of the ScrollFrame with default settings.\n"
                 "Try scrolling with your trackpad or using the scrollbar.",
            wraplength=800,
            justify="left"
        ).pack(fill="x", pady=(0, 10))
        
        # Create a ScrollFrame with default settings
        scroll_frame = ScrollFrame(tab, bg="#0a0a0a")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add a lot of content to make it scrollable
        for i in range(1, 51):
            frame = ttk.Frame(scroll_frame.scrollable_frame)
            frame.pack(fill="x", padx=10, pady=5)
            
            ttk.Label(
                frame,
                text=f"Item {i}",
                foreground="#FFFFFF",
                font=("Segoe UI", 10, "bold")
            ).pack(side="left", padx=5)
            
            ttk.Label(
                frame,
                text=f"This is item {i} in the scrollable frame. Scroll to see more items.",
                foreground="#c0c0c0"
            ).pack(side="left", padx=5)
    
    def _create_options_demo_tab(self, notebook):
        """Create a tab demonstrating different configuration options."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Configuration Options")
        
        # Add description
        desc_frame = ttk.Frame(tab)
        desc_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(
            desc_frame,
            text="ScrollFrame Configuration Options",
            style="Subtitle.TLabel"
        ).pack(anchor="w")
        
        ttk.Label(
            desc_frame,
            text="This tab demonstrates different configuration options for the ScrollFrame.\n"
                 "Each example shows a different configuration possibility.",
            wraplength=800,
            justify="left"
        ).pack(fill="x", pady=(0, 10))
        
        # Create a frame to hold multiple ScrollFrame examples side by side
        examples_frame = ttk.Frame(tab)
        examples_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Example 1: Default scrollbar on right
        example1_frame = ttk.LabelFrame(examples_frame, text="Default (Scrollbar Right)")
        example1_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        scroll1 = ScrollFrame(example1_frame)
        scroll1.pack(fill="both", expand=True, padx=5, pady=5)
        
        self._add_sample_content(scroll1.scrollable_frame, 30)
        
        # Example 2: Scrollbar on left
        example2_frame = ttk.LabelFrame(examples_frame, text="Scrollbar Left")
        example2_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        scroll2 = ScrollFrame(example2_frame, scrollbar_side="left")
        scroll2.pack(fill="both", expand=True, padx=5, pady=5)
        
        self._add_sample_content(scroll2.scrollable_frame, 30)
        
        # Example 3: Auto-hide scrollbar
        example3_frame = ttk.LabelFrame(examples_frame, text="Auto-hide Scrollbar")
        example3_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        scroll3 = ScrollFrame(example3_frame, hide_scrollbar=True)
        scroll3.pack(fill="both", expand=True, padx=5, pady=5)
        
        self._add_sample_content(scroll3.scrollable_frame, 30)
    
    def _create_content_demo_tab(self, notebook):
        """Create a tab demonstrating different types of content in the ScrollFrame."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Content Examples")
        
        # Add description
        desc_frame = ttk.Frame(tab)
        desc_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(
            desc_frame,
            text="ScrollFrame with Different Content Types",
            style="Subtitle.TLabel"
        ).pack(anchor="w")
        
        ttk.Label(
            desc_frame,
            text="This tab demonstrates how ScrollFrame works with different types of content.\n"
                 "Try scrolling through the different widgets and content types.",
            wraplength=800,
            justify="left"
        ).pack(fill="x", pady=(0, 10))
        
        # Create a ScrollFrame with mixed content
        scroll_frame = ScrollFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add a variety of widgets to the scrollable frame
        content_frame = scroll_frame.scrollable_frame
        
        # 1. Text heading
        ttk.Label(
            content_frame,
            text="Mixed Content Example",
            font=("Segoe UI", 16, "bold"),
            foreground="#00b4d8"
        ).pack(fill="x", padx=10, pady=(20, 10))
        
        # 2. Text paragraph
        ttk.Label(
            content_frame,
            text="This example shows how the ScrollFrame can handle different types of content, "
                 "including text, images, buttons, entry fields, and other complex widgets. "
                 "Scroll down to see more content types.",
            wraplength=700,
            justify="left"
        ).pack(fill="x", padx=20, pady=10)
        
        # 3. Buttons section
        buttons_frame = ttk.LabelFrame(content_frame, text="Buttons Example")
        buttons_frame.pack(fill="x", padx=20, pady=15)
        
        buttons_container = ttk.Frame(buttons_frame)
        buttons_container.pack(fill="x", padx=10, pady=10)
        
        for i in range(5):
            ttk.Button(
                buttons_container,
                text=f"Button {i+1}",
                style="Action.TButton"
            ).pack(side="left", padx=5)
        
        # 4. Form example
        form_frame = ttk.LabelFrame(content_frame, text="Form Elements")
        form_frame.pack(fill="x", padx=20, pady=15)
        
        form_fields = [
            ("Name", tk.StringVar()),
            ("Email", tk.StringVar()),
            ("Phone", tk.StringVar()),
            ("Address", tk.StringVar())
        ]
        
        for label_text, var in form_fields:
            field_frame = ttk.Frame(form_frame)
            field_frame.pack(fill="x", padx=10, pady=5)
            
            ttk.Label(
                field_frame,
                text=f"{label_text}:",
                width=15
            ).pack(side="left", padx=5)
            
            ttk.Entry(
                field_frame,
                textvariable=var,
                width=40
            ).pack(side="left", fill="x", expand=True, padx=5)
        
        # 5. Checkboxes
        check_frame = ttk.LabelFrame(content_frame, text="Options")
        check_frame.pack(fill="x", padx=20, pady=15)
        
        options = [
            ("Enable feature 1", tk.BooleanVar(value=True)),
            ("Enable feature 2", tk.BooleanVar(value=False)),
            ("Enable feature 3", tk.BooleanVar(value=True)),
            ("Enable feature 4", tk.BooleanVar(value=False))
        ]
        
        for option_text, var in options:
            ttk.Checkbutton(
                check_frame,
                text=option_text,
                variable=var
            ).pack(anchor="w", padx=15, pady=5)
        
        # 6. More text to ensure scrolling is needed
        for i in range(10):
            ttk.Label(
                content_frame,
                text=f"Additional content section {i+1}. This is added to ensure the content "
                     f"is long enough to demonstrate scrolling capabilities.",
                wraplength=700,
                justify="left"
            ).pack(fill="x", padx=20, pady=10)
    
    def _create_scrolling_methods_tab(self, notebook):
        """Create a tab demonstrating different scrolling methods and controls."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Scrolling Controls")
        
        # Add description
        desc_frame = ttk.Frame(tab)
        desc_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(
            desc_frame,
            text="ScrollFrame Scrolling Methods",
            style="Subtitle.TLabel"
        ).pack(anchor="w")
        
        ttk.Label(
            desc_frame,
            text="This tab demonstrates different methods to control scrolling programmatically.\n"
                 "Use the buttons below to control the scrolling position.",
            wraplength=800,
            justify="left"
        ).pack(fill="x", pady=(0, 10))
        
        # Split into control panel and scroll view
        split_frame = ttk.Frame(tab)
        split_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Control panel on the left
        control_frame = ttk.LabelFrame(split_frame, text="Scroll Controls")
        control_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # ScrollFrame on the right
        scroll_demo_frame = ttk.Frame(split_frame)
        scroll_demo_frame.pack(side="left", fill="both", expand=True)
        
        # Create the ScrollFrame instance we'll control
        self.scroll_frame = ScrollFrame(scroll_demo_frame)
        self.scroll_frame.pack(fill="both", expand=True)
        
        # Add lots of numbered content to make scrolling obvious
        self._add_sample_content(self.scroll_frame.scrollable_frame, 50)
        
        # Add control buttons
        ttk.Button(
            control_frame,
            text="Scroll to Top",
            command=self.scroll_frame.scroll_to_top
        ).pack(fill="x", padx=10, pady=5)
        
        ttk.Button(
            control_frame,
            text="Scroll to Bottom",
            command=self.scroll_frame.scroll_to_bottom
        ).pack(fill="x", padx=10, pady=5)
        
        ttk.Label(
            control_frame,
            text="Scroll to Position:"
        ).pack(padx=10, pady=(15, 5))
        
        positions = [0, 0.25, 0.5, 0.75, 1.0]
        for pos in positions:
            pos_text = f"{int(pos * 100)}%" 
            ttk.Button(
                control_frame,
                text=pos_text,
                command=lambda p=pos: self.scroll_frame.scroll_to_position(p)
            ).pack(fill="x", padx=10, pady=2)
    
    def _add_sample_content(self, parent, count=20):
        """Add sample content items to a parent widget."""
        for i in range(1, count + 1):
            frame = ttk.Frame(parent)
            frame.pack(fill="x", padx=10, pady=5)
            
            ttk.Label(
                frame,
                text=f"Item {i}",
                foreground="#FFFFFF",
                font=("Segoe UI", 10, "bold"),
                width=10
            ).pack(side="left", padx=5)
            
            ttk.Label(
                frame,
                text=f"This is content item {i}. Scroll to see more items below.",
                foreground="#c0c0c0"
            ).pack(side="left", padx=5, fill="x", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScrollFrameDemo(root)
    root.mainloop() 