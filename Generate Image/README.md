# AI Video Generator with Hugging Face Integration

A modern web application that converts images into videos using AI, featuring **Hugging Face model integration** for enhanced prompt generation.

## 🤖 Features

### 🎨 Modern Interface
- **Clean Design**: Professional, responsive interface
- **Real-time Feedback**: Progress tracking and notifications
- **Mobile Friendly**: Works on all devices

### 🧠 AI-Powered Prompt Enhancement
- **Hugging Face Integration**: Uses `shreyahegde/video_prompt_generation` model
- **Smart Prompt Enhancement**: Automatically improves user prompts
- **T5-Based Model**: Fine-tuned for video generation prompts
- **Fallback System**: Works even if AI model isn't available

### 🖼️ Image Processing
- **Drag & Drop**: Easy image upload
- **Format Support**: JPG, PNG, GIF, WebP
- **Preview**: Live image preview before processing
- **Smart Validation**: Automatic file type checking

### ⚙️ Customizable Settings
- **Duration**: 3, 5, or 10 seconds
- **Quality**: 720p, 1080p, 4K
- **Style**: Realistic, Cinematic, Artistic, Anime
- **Frame Rate**: 24, 30, or 60 FPS

### 🎬 Enhanced Video Generation
- **AI-Enhanced Effects**: Based on improved prompts
- **Progress Tracking**: Visual progress with step-by-step updates
- **Prompt Comparison**: Shows original vs enhanced prompts
- **Model Status**: Displays whether AI model is active

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Application**
   ```bash
   python app.py
   ```

3. **Open in Browser**
   Navigate to `http://localhost:5000`

## 📋 Requirements

- **Python 3.8+**
- **2GB+ RAM** (for AI model)
- **Internet connection** (for model download)
- **Optional**: CUDA-compatible GPU for faster processing

## 🎯 How to Use

### Basic Workflow
1. **Upload an image** by dragging and dropping or clicking to browse
2. **Enter a prompt** describing your desired video transformation
3. **AI Enhancement**: The system automatically enhances your prompt using the Hugging Face model
4. **Adjust settings** (duration, quality, style, frame rate)
5. **Generate video** and download the AI-enhanced result
6. **Compare prompts** to see how AI improved your description

### Example Usage (Based on Server Logs)
✅ **Successfully tested endpoints:**
- `/api/status` - Check system and model status
- `/api/enhance-prompt` - AI prompt enhancement working
- `/api/generate-video` - Video generation successful
- `/api/download` - Video download functional

### Example Prompts

#### Simple Input → AI Enhanced Output
- **Input**: "make it move"
- **Enhanced**: "make it move with smooth cinematic motion, dynamic lighting"

- **Input**: "add effects"
- **Enhanced**: "add magical particle effects, glowing elements, cinematic style"

- **Input**: "zoom in"
- **Enhanced**: "cinematic zoom in effect with dramatic focus, professional camera movement"

## 🔧 Technical Details

### AI Model Integration
- **Model**: `shreyahegde/video_prompt_generation`
- **Base**: Fine-tuned T5 (Text-to-Text Transfer Transformer)
- **Framework**: Hugging Face Transformers
- **Purpose**: Enhances user prompts for better video generation

### Backend Architecture
- **Flask**: Python web framework
- **Transformers**: Hugging Face model integration
- **OpenCV**: Video processing
- **PIL**: Image manipulation
- **PyTorch**: AI model runtime

### File Structure
```
Generate Image/
├── index.html               # Frontend interface
├── style.css                # Clean, modern styling
├── script.js                # Frontend with API integration
├── app.py                   # Flask backend with AI model
├── requirements.txt         # Python dependencies
├── README.md               # This documentation
├── uploads/                # Image upload directory
├── outputs/                # Generated video directory
└── video_prompt_generation/ # Hugging Face model cache
```

## ⚡ AI Model Features

### Prompt Enhancement Process
1. **Input Analysis**: Analyzes user's original prompt
2. **Context Understanding**: Considers image content (basic analysis)
3. **Enhancement Generation**: Uses T5 model to improve prompt
4. **Style Integration**: Adds appropriate visual effects keywords
5. **Output Optimization**: Returns enhanced prompt for video generation

### Model Performance
- **Size**: 248M parameters
- **Architecture**: T5-base fine-tuned
- **Training**: 5 epochs with Adam optimizer
- **Fallback**: Graceful degradation if model unavailable

## 🛠️ Customization

### Adding New Enhancement Patterns
1. **Modify `enhance_prompt()` in `app.py`**
2. **Update fallback enhancement patterns**
3. **Add new effect detection keywords**

### Model Configuration
```python
# In app.py, modify VideoPromptGenerator class
self.generator = pipeline(
    "text2text-generation",
    model=self.model,
    tokenizer=self.tokenizer,
    max_new_tokens=256,  # Use max_new_tokens instead of max_length
    temperature=0.7,     # Control creativity
    do_sample=True       # Enable sampling
)
```

**Note**: Use `max_new_tokens` instead of `max_length` to avoid configuration warnings.

## 🔍 API Endpoints

### `/api/enhance-prompt` (POST)
Enhance a text prompt using the AI model
```json
{
  "prompt": "make the image move"
}
```

### `/api/generate-video` (POST)
Generate video with enhanced prompts
- Accepts: multipart/form-data with image and parameters
- Returns: Video file and enhancement details

### `/api/status` (GET)
Get system and model status
```json
{
  "status": "online",
  "model_loaded": true,
  "device": "cuda:0",
  "model_name": "shreyahegde/video_prompt_generation"
}
```

### `/api/download/{filename}` (GET)
Download generated video files
- Returns: Video file (MP4) with proper HTTP range support
- Supports partial content requests for streaming

## ❗ Notes & Troubleshooting

- **Working AI Integration**: Successfully generates videos with Hugging Face prompt enhancement
- **Model Dependency**: Requires internet for initial model download
- **Processing Time**: AI enhancement adds ~1-2 seconds
- **GPU Recommended**: CPU-only processing is slower
- **Video Generation**: Creates actual video files that can be downloaded

### Common Issues:

#### Video Generation Shows No Output
If video generation appears to complete but no video is produced:

1. **Check Server Logs**: Look for error messages in the terminal
2. **Verify OpenCV Installation**: Run `pip install opencv-python` if needed
3. **Check Output Directory**: Videos are saved in `outputs/` folder
4. **Codec Issues**: The app automatically tries multiple codecs (mp4v, XVID, MJPG)
5. **Color Change Prompts**: Try "change its color to green" - now properly supported!

#### Supported Effects:
- ✅ **Zoom**: "zoom in", "closer", "approach"
- ✅ **Particles**: "particles", "sparkles", "magical effects"  
- ✅ **Color Changes**: "change color to green/red/blue", "green tint"
- ✅ **Pan/Movement**: "pan left", "slide", "move"
- ✅ **Rotation**: "rotate", "spin", "turn"
- ✅ **Blur/Focus**: "blur", "focus pull", "depth"
- ✅ **Fade**: "fade in", "appear", "dissolve"
- ✅ **Wave**: "wave effect", "ripple", "flow"
- ✅ **Cinematic**: "cinematic", "dramatic lighting"

#### Server Logs to Monitor:
```bash
# Look for these debug messages:
Processing video request for: [your prompt]
Detected effects: {'zoom': True, 'color_shift': True, 'color_target': (0, 255, 0)}
Generated X frames
Using codec: mp4v
Video created successfully: outputs/[filename]
Video file size: X bytes
```

#### Manual Verification:
```bash
# Check if videos are being created
ls outputs/
# Check video file sizes
ls -la outputs/
```

## 🔮 Real AI Video Generation

This interface is ready for integration with actual video generation models like:

1. **Stable Video Diffusion**
2. **AnimateDiff**
3. **Pika Labs API**
4. **RunwayML API**

The prompt enhancement system will improve results with any of these models.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test with the Hugging Face model
4. Submit a pull request

## 📄 License

MIT License - feel free to use and modify

---

**🎬 Create amazing AI-enhanced videos with intelligent prompt generation!**
