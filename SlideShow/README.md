# Advanced Image Slideshow

A feature-rich image slideshow application built with Python and Tkinter that provides an elegant way to view and manage your image collections.

## Features

### Core Functionality
- **Automatic Slideshow**: Images automatically advance at configurable intervals
- **Manual Navigation**: Navigate through images using buttons or keyboard shortcuts
- **Image Aspect Ratio Preservation**: Images are resized while maintaining their original proportions
- **Multiple Image Format Support**: JPG, JPEG, PNG, GIF, BMP, and TIFF formats

### Advanced Features
- **Fullscreen Mode**: Toggle between windowed and fullscreen viewing
- **Thumbnail Gallery**: Quick navigation through a scrollable thumbnail view
- **Shuffle Mode**: Randomize the order of images
- **Speed Control**: Choose between 1-second and 2-second intervals
- **Progress Tracking**: Visual progress bar and image counter
- **Add Images**: Dynamically add more images to the slideshow
- **Keyboard Shortcuts**: Full keyboard navigation support

## Screenshots

![Slideshow Interface](screenshot.png)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application
```bash
python slideshow.py
```

### Default Images
The application looks for default images in the current directory:
- `image1.jpg`
- `image2.jpg` 
- `image3.jpg`

### Controls

#### Button Controls
- **▶ Play/⏸ Pause**: Start or stop the automatic slideshow
- **⏮ Previous Pic**: Go to the previous image
- **Next Pic ⏭**: Go to the next image
- **🔀 Shuffle**: Randomize the image order
- **➕ Add Images**: Browse and add more images to the slideshow
- **⛶ Fullscreen**: Toggle fullscreen mode
- **🖼 Thumbnails**: Open thumbnail gallery for quick navigation

#### Keyboard Shortcuts
- **Left Arrow**: Previous image
- **Right Arrow**: Next image
- **Spacebar**: Toggle play/pause
- **F11 or F**: Toggle fullscreen mode
- **Escape**: Exit fullscreen mode

#### Speed Settings
- **1s**: Images change every 1 second
- **2s**: Images change every 2 seconds (default)

## File Structure
```
SlideShow/
├── slideshow.py          # Main application file
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── image1.jpg           # Sample image 1
├── image2.jpg           # Sample image 2
└── image3.jpg           # Sample image 3
```

## Technical Details

### Built With
- **Python 3.x**: Core programming language
- **Tkinter**: GUI framework (included with Python)
- **Pillow (PIL)**: Image processing library
- **itertools**: For cycling through images

### Key Components
- **ImageSlideshow Class**: Main application class
- **Image Processing**: Automatic resizing with aspect ratio preservation
- **Event Handling**: Keyboard and mouse event management
- **Timer Management**: Automatic slideshow progression

## Customization

### Changing Default Settings
Edit the following variables in `slideshow.py`:

```python
# Window size
self.root.geometry("1000x700")

# Default slide interval (milliseconds)
self.slide_interval = 2000

# Maximum display size (width, height)
self.max_display_size = (600, 400)
```

### Adding New Image Formats
To support additional image formats, update the file types in the `add_images()` method:

```python
file_types = [
    ('Image files', '*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp'),
    ('All files', '*.*')
]
```

## Troubleshooting

### Common Issues

1. **Images not loading**
   - Ensure image files exist in the correct directory
   - Check that image formats are supported
   - Verify file permissions

2. **Keyboard shortcuts not working**
   - Click on the main window to ensure it has focus
   - Check that no other application is capturing the key events

3. **Performance issues with large images**
   - Large images are automatically resized for display
   - Consider reducing the `max_display_size` for better performance

### Error Messages
- **"No valid images found"**: No supported image files were found in the directory
- **"No images to display!"**: Attempting to start slideshow without loaded images

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built as part of the "50 Python Projects for Beginners" series
- Uses the Pillow library for image processing
- Tkinter for the graphical user interface


## Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Enjoy your slideshow experience!** 🖼️✨
