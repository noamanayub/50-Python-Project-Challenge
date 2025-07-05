from itertools import cycle
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import random
import time

class ImageSlideshow:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Slideshow")
        # Increase window size for better visibility
        self.root.geometry("1000x700")
        
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.image_paths = []
        self.current_images = []
        self.photo_images = []
        self.slideshow_iterator = None
        self.current_index = 0
        self.is_playing = False
        self.slide_interval = 2000  # milliseconds (2 seconds)
        self.timer_id = None
        self.max_display_size = (600, 400)  # Smaller display size
        self.fullscreen = False
        self.transition_speed = 0.01  # Faster transition
        self.thumb_window = None  # for thumbnail gallery
        
        # Load default images
        self.load_default_images()
        
        # Create GUI
        self.create_widgets()
        
        # Setup keyboard bindings
        self.setup_keyboard_bindings()
        
        # Initialize slideshow
        self.load_images()
        
    def load_default_images(self):
        """Load default images from the SlideShow folder"""
        default_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
        for path in default_paths:
            # Try current directory first
            if os.path.exists(path):
                self.image_paths.append(path)
            else:
                # Try SlideShow subfolder
                full_path = os.path.join("SlideShow", path)
                if os.path.exists(full_path):
                    self.image_paths.append(full_path)
        
        # If no images found, create some test entries
        if not self.image_paths:
            self.image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Button style - MOVED UP HERE before first use
        button_style = {'font': ('Arial', 10, 'bold'), 'bg': '#3498db', 'fg': 'white',
                       'activebackground': '#2980b9', 'activeforeground': 'white',
                       'relief': tk.RAISED, 'bd': 2, 'padx': 10, 'pady': 5}
    
        # Title
        title_label = tk.Label(main_frame, text="Advanced Image Slideshow", 
                              font=('Arial', 24, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Image display frame
        image_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        image_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.image_label = tk.Label(image_frame, bg='#34495e', text="No Image Loaded", 
                                   font=('Arial', 16), fg='#bdc3c7')
        self.image_label.pack(expand=True)
        
        # New button panel below the image
        button_panel = tk.Frame(main_frame, bg='#2c3e50')
        button_panel.pack(fill=tk.X, pady=(0, 10))
        
        # Play/Pause button
        self.play_button = tk.Button(button_panel, text="▶ Play", command=self.toggle_slideshow, **button_style)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        # Previous button
        self.back_button = tk.Button(button_panel, text="⏮ Previous Pic", command=self.previous_image, **button_style)
        self.back_button.pack(side=tk.LEFT, padx=5)
        
        # Next button
        self.next_button = tk.Button(button_panel, text="Next Pic ⏭", command=self.next_image, **button_style)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Control frame
        control_frame = tk.Frame(main_frame, bg='#2c3e50')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Control buttons (only non-duplicate ones)
        self.shuffle_button = tk.Button(control_frame, text="🔀 Shuffle", command=self.shuffle_images, **button_style)
        self.shuffle_button.pack(side=tk.LEFT, padx=5)
        
        self.add_button = tk.Button(control_frame, text="➕ Add Images", command=self.add_images, **button_style)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        # Fullscreen button
        self.fullscreen_button = tk.Button(control_frame, text="⛶ Fullscreen", command=self.toggle_fullscreen, **button_style)
        self.fullscreen_button.pack(side=tk.LEFT, padx=5)

        # Create thumbnail gallery button
        self.thumbs_button = tk.Button(control_frame, text="🖼 Thumbnails", command=self.show_thumbnails, **button_style)
        self.thumbs_button.pack(side=tk.LEFT, padx=5)
        
        # Settings frame
        settings_frame = tk.Frame(main_frame, bg='#2c3e50')
        settings_frame.pack(fill=tk.X)
        
        # Speed control
        speed_label = tk.Label(settings_frame, text="Speed:", font=('Arial', 10), fg='#ecf0f1', bg='#2c3e50')
        speed_label.pack(side=tk.LEFT, padx=5)
        
        self.speed_var = tk.IntVar(value=self.slide_interval)
        for label, val in [("1s", 1000), ("2s", 2000)]:
            rb = tk.Radiobutton(
                settings_frame, text=label, variable=self.speed_var, value=val,
                command=self.update_speed, bg='#2c3e50', fg='#ecf0f1', selectcolor='#34495e'
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Image counter
        self.counter_label = tk.Label(settings_frame, text="0/0", font=('Arial', 10), 
                                     fg='#ecf0f1', bg='#2c3e50')
        self.counter_label.pack(side=tk.RIGHT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(settings_frame, length=200, mode='determinate')
        self.progress.pack(side=tk.RIGHT, padx=10)
    
    def resize_image_maintain_aspect(self, image, max_size):
        """Resize image while maintaining aspect ratio"""
        image_size = image.size
        max_width, max_height = max_size
        
        # Calculate aspect ratio
        aspect_ratio = image_size[0] / image_size[1]
        
        # Calculate new dimensions
        if aspect_ratio > 1:  # Landscape
            new_width = min(max_width, image_size[0])
            new_height = int(new_width / aspect_ratio)
        else:  # Portrait or square
            new_height = min(max_height, image_size[1])
            new_width = int(new_height * aspect_ratio)
        
        # Ensure dimensions don't exceed max_size
        if new_width > max_width:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
        if new_height > max_height:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def load_images(self):
        """Load and process images"""
        self.current_images = []
        self.photo_images = []
        
        valid_paths = []
        for path in self.image_paths:
            try:
                if os.path.exists(path):
                    image = Image.open(path)
                    resized_image = self.resize_image_maintain_aspect(image, self.max_display_size)
                    photo_image = ImageTk.PhotoImage(resized_image)
                    
                    self.current_images.append(resized_image)
                    self.photo_images.append(photo_image)
                    valid_paths.append(path)
            except Exception as e:
                print(f"Error loading image {path}: {e}")
        
        self.image_paths = valid_paths
        
        if self.photo_images:
            self.slideshow_iterator = cycle(self.photo_images)
            self.current_index = 0
            self.show_current_image()
            self.update_counter()
            # Auto-start slideshow
            self.start_slideshow()
        else:
            self.image_label.config(image="", text="No valid images found")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen or windowed mode."""
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self):
        """Exit fullscreen mode."""
        if self.fullscreen:
            self.fullscreen = False
            self.root.attributes("-fullscreen", False)
    
    def show_current_image(self):
        """Display the current image"""
        if self.photo_images:
            self.image_label.config(image=self.photo_images[self.current_index], text="")
            self.update_progress()
    
    def update_counter(self):
        """Update the image counter"""
        total = len(self.photo_images)
        current = self.current_index + 1 if self.photo_images else 0
        self.counter_label.config(text=f"{current}/{total}")
    
    def update_progress(self):
        """Update the progress bar"""
        if self.photo_images:
            progress_value = (self.current_index / len(self.photo_images)) * 100
            self.progress['value'] = progress_value
    
    def update_speed(self, event=None):
        """Update slideshow speed"""
        self.slide_interval = self.speed_var.get()
        if self.is_playing:
            self.stop_slideshow()
            self.start_slideshow()
    
    def toggle_slideshow(self):
        """Toggle between play and pause"""
        if self.is_playing:
            self.stop_slideshow()
        else:
            self.start_slideshow()
    
    def start_slideshow(self):
        """Start the slideshow"""
        if not self.photo_images:
            messagebox.showwarning("Warning", "No images to display!")
            return
        
        self.is_playing = True
        self.play_button.config(text="⏸ Pause")
        self.auto_advance()
    
    def stop_slideshow(self):
        """Stop the slideshow"""
        self.is_playing = False
        self.play_button.config(text="▶ Play")
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def auto_advance(self):
        """Automatically advance to next image"""
        if self.is_playing and self.photo_images:
            self.next_image()
            self.timer_id = self.root.after(self.slide_interval, self.auto_advance)
    
    def next_image(self):
        """Show next image"""
        if self.photo_images:
            self.current_index = (self.current_index + 1) % len(self.photo_images)
            self.show_current_image()
            self.update_counter()
    
    def previous_image(self):
        """Show previous image"""
        if self.photo_images:
            self.current_index = (self.current_index - 1) % len(self.photo_images)
            self.show_current_image()
            self.update_counter()
    
    def shuffle_images(self):
        """Shuffle the image order"""
        if len(self.photo_images) > 1:
            # Create list of indices
            indices = list(range(len(self.photo_images)))
            random.shuffle(indices)
            
            # Reorder images and paths
            self.photo_images = [self.photo_images[i] for i in indices]
            self.current_images = [self.current_images[i] for i in indices]
            self.image_paths = [self.image_paths[i] for i in indices]
            
            self.current_index = 0
            self.show_current_image()
            self.update_counter()
            messagebox.showinfo("Success", "Images shuffled!")
    
    def add_images(self):
        """Add more images to the slideshow"""
        file_types = [
            ('Image files', '*.jpg *.jpeg *.png *.gif *.bmp *.tiff'),
            ('All files', '*.*')
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=file_types
        )
        
        if files:
            self.image_paths.extend(files)
            self.load_images()
            messagebox.showinfo("Success", f"Added {len(files)} image(s)!")
    
    def show_thumbnails(self):
        """Open or update a thumbnail gallery in a separate window."""
        if self.thumb_window and self.thumb_window.winfo_exists():
            self.thumb_window.lift()
            return
        
        self.thumb_window = tk.Toplevel(self.root)
        self.thumb_window.title("Thumbnails")
        self.thumb_window.geometry("600x400")
        
        # Create scrollable frame
        canvas = tk.Canvas(self.thumb_window, bg='#2c3e50')
        scrollbar = tk.Scrollbar(self.thumb_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2c3e50')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add thumbnails
        for idx, photo in enumerate(self.photo_images):
            # Create smaller thumbnail
            original_img = self.current_images[idx]
            thumb_img = original_img.resize((100, 100), Image.Resampling.LANCZOS)
            thumb_photo = ImageTk.PhotoImage(thumb_img)
            
            btn = tk.Button(scrollable_frame, image=thumb_photo, 
                          command=lambda i=idx: self.select_thumbnail(i),
                          bg='#34495e', relief=tk.RAISED, bd=2)
            btn.image = thumb_photo  # Keep a reference
            btn.grid(row=idx // 5, column=idx % 5, padx=5, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_thumbnail(self, index):
        """Select and display an image from the thumbnail gallery."""
        if 0 <= index < len(self.photo_images):
            self.current_index = index
            self.show_current_image()
            self.update_counter()
            if self.thumb_window and self.thumb_window.winfo_exists():
                self.thumb_window.destroy()  # Close the thumbnail window
    
    def setup_keyboard_bindings(self):
        """Setup keyboard shortcuts for navigation"""
        self.root.bind('<Left>', lambda e: self.previous_image())
        self.root.bind('<Right>', lambda e: self.next_image())
        self.root.bind('<space>', lambda e: self.toggle_slideshow())
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen())
        self.root.bind('<f>', lambda e: self.toggle_fullscreen())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.focus_set()  # Make sure window can receive key events

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSlideshow(root)
    root.mainloop()
