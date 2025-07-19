# Real-Time Object Detection and Tracking System

This project implements a real-time object detection and tracking system using the YOLOv8 model. The system can detect and track various objects in a video stream, estimate their speed, and display the count of moving and stationary objects.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features

- Real-time object detection and tracking using YOLOv8.
- Speed estimation of moving objects in meters per second (m/s).
- Display of the count of moving and stationary objects.
- Resizing of video frames for better visualization.

## Requirements

- Python 3.7 or higher
- Required Python packages listed in `requirements.txt`

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/noamanayub/50-Python-Project-Challenge
   cd 50-Python-Project-Challenge
   ```

2. **Create a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv myenv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Main Script**:
   ```bash
   python main.py
   ```

2. **Input Video**:
   - The script expects a video file named `test.mp4` in the project directory. You can modify the `video_path` variable in `main.py` to use a different video file.

3. **Output**:
   - The script will display the video stream with bounding boxes around detected objects, their speeds, and the count of moving and stationary objects.
   - Press `q` to exit the video stream.

## Configuration

- **Model Path**: The YOLOv8 model is loaded from `yolov8n.pt`. Ensure this file is in the same directory as `main.py` or provide the correct path.
- **Video Path**: The video file path is set to `./test.mp4`. Modify this in `main.py` if you want to use a different video file.
- **Detection Thresholds**: The confidence and NMS thresholds can be adjusted in `main.py` to improve detection accuracy.

## Troubleshooting

- **ModuleNotFoundError**: Ensure all dependencies are installed correctly by running `pip install -r requirements.txt`.
- **Video Capture Issues**: Ensure the video file path is correct and the file is accessible.
- **Performance Issues**: If the system is running slowly, consider reducing the video frame size or using a more powerful GPU.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.


### Summary
This updated `README.md` file provides a comprehensive guide to your project, including installation instructions, usage guidelines, configuration options, and troubleshooting tips. It helps users and contributors understand and use your project effectively without including the license section.