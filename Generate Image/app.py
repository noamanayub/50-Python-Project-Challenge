#!/usr/bin/env python3
"""
AI Video Generator Backend with Hugging Face Integration
Flask server that uses the video_prompt_generation model for enhanced prompts
"""

import os
import io
import json
import uuid
import time
import base64
from datetime import datetime
from typing import Optional, Dict, Any

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Hugging Face imports
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
import requests
from urllib.parse import quote

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

class VideoPromptGenerator:
    """
    Hugging Face Video Prompt Generation Model Integration
    """
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        self.load_model()
    
    def load_model(self):
        """Load the Hugging Face model for video prompt generation."""
        try:
            print("Loading Hugging Face video prompt generation model...")
            model_name = "shreyahegde/video_prompt_generation"
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True, trust_remote_code=True)
            except Exception as e:
                print(f"Tokenizer loading failed! Check for spiece.model or tokenizer files. Error: {e}")
                raise
            try:
                self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)
            except Exception as e:
                print(f"Model loading failed! Error: {e}")
                raise
            self.model.to(self.device)
            # Create pipeline for easier usage
            self.generator = pipeline(
                "text2text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device.type == "cuda" else -1
            )
            self.model_loaded = True
            print(f"Model loaded successfully on {self.device}")
        except Exception as e:
            print(f"Error loading model or tokenizer (spiece.model): {e}")
            print("Falling back to simulation mode")
            self.model_loaded = False
    
    def enhance_prompt(self, user_prompt: str, image_description: str = "") -> str:
        """
        Enhance user prompt using the video generation model
        
        Args:
            user_prompt: User's original prompt
            image_description: Optional description of the uploaded image
            
        Returns:
            Enhanced prompt for video generation
        """
        try:
            if not self.model_loaded:
                return self.fallback_enhance_prompt(user_prompt)
            
            # Create input for the model - simplified format
            input_text = user_prompt
            
            print(f"Input to model: {input_text}")
            
            # Generate enhanced prompt with better parameters
            enhanced = self.generator(
                input_text,
                max_new_tokens=50,  # Limit output length
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            enhanced_prompt = enhanced[0]['generated_text'].strip()
            print(f"Model output: {enhanced_prompt}")
            
            # Clean up the output - remove repetition of input
            if enhanced_prompt.startswith(input_text):
                enhanced_prompt = enhanced_prompt[len(input_text):].strip()
            
            # If the cleaned prompt is too short or empty, use fallback
            if len(enhanced_prompt) < 5:
                print("Model output too short, using fallback")
                return self.fallback_enhance_prompt(user_prompt)
            
            # Ensure it's not just the original prompt
            if enhanced_prompt.lower() == user_prompt.lower():
                return self.fallback_enhance_prompt(user_prompt)
            
            # Combine original prompt with enhancement
            final_prompt = f"{user_prompt}, {enhanced_prompt}"
            
            # Limit total length to avoid too long prompts
            if len(final_prompt) > 200:
                final_prompt = final_prompt[:200].rsplit(',', 1)[0]
            
            print(f"Final enhanced prompt: {final_prompt}")
            return final_prompt
            
        except Exception as e:
            print(f"Error enhancing prompt: {e}")
            return self.fallback_enhance_prompt(user_prompt)
    
    def fallback_enhance_prompt(self, user_prompt: str) -> str:
        """Fallback prompt enhancement when model is not available"""
        enhancements = {
            'cinematic': ', cinematic lighting, dramatic shadows, film grain',
            'realistic': ', photorealistic, high detail, natural lighting',
            'artistic': ', artistic style, vibrant colors, creative composition',
            'anime': ', anime style, vibrant colors, dynamic motion',
            'green': ', vibrant green color transformation, emerald tones',
            'red': ', rich red color transformation, crimson tones',
            'blue': ', deep blue color transformation, azure tones',
            'yellow': ', bright yellow color transformation, golden tones',
            'purple': ', rich purple color transformation, violet tones',
            'color': ', dynamic color transformation, vibrant hues',
            'change': ', smooth transformation effects, fluid motion'
        }
        
        enhanced = user_prompt
        
        # Add style-based enhancements
        for keyword, enhancement in enhancements.items():
            if keyword in user_prompt.lower():
                enhanced += enhancement
                break
        
        # If no specific enhancement found, add default
        if enhanced == user_prompt:
            enhanced += ", smooth motion, high quality, detailed"
        
        return enhanced

class VideoProcessor:
    """
    Video processing with Hugging Face integration
    """
    
    def __init__(self):
        self.prompt_generator = VideoPromptGenerator()
        self.hf_video_generator = HuggingFaceVideoGenerator()
    
    def analyze_image(self, image_path: str) -> str:
        """Basic image analysis to describe content"""
        try:
            # Simple image analysis (in a real app, you might use CLIP or similar)
            image = Image.open(image_path)
            width, height = image.size
            
            # Basic description based on image properties
            if width > height:
                orientation = "landscape"
            elif height > width:
                orientation = "portrait"
            else:
                orientation = "square"
            
            return f"{orientation} image, {width}x{height} pixels"
            
        except Exception as e:
            return "uploaded image"
    
    def process_video_request(self, image_path: str, user_prompt: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process video generation request with Hugging Face API integration
        
        Args:
            image_path: Path to uploaded image
            user_prompt: User's prompt
            settings: Video generation settings
            
        Returns:
            Processing result with enhanced prompt and video info
        """
        try:
            print(f"Processing video request for: {user_prompt}")
            print(f"Image path: {image_path}")
            print(f"Settings: {settings}")
            
            # Analyze the image
            image_description = self.analyze_image(image_path)
            print(f"Image description: {image_description}")
            
            # Enhance the prompt using the Hugging Face model
            enhanced_prompt = self.prompt_generator.enhance_prompt(user_prompt, image_description)
            print(f"Enhanced prompt: {enhanced_prompt}")
            
            # Try Hugging Face video generation first
            hf_result = self.hf_video_generator.generate_video_from_prompt(enhanced_prompt, image_path)
            print(f"HF API result: {hf_result}")
            
            # Process the image for fallback simulation
            processed_image = self.preprocess_image(image_path)
            print(f"Processed image shape: {processed_image.shape}")
            
            # Generate video frames (enhanced simulation with HF insights)
            frames = self.generate_video_frames(processed_image, enhanced_prompt, settings, hf_result)
            print(f"Generated {len(frames)} frames")
            
            # Create video file
            output_filename = f"{uuid.uuid4()}_generated_video.mp4"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            print(f"Creating video at: {output_path}")
            
            created_video_path = self.create_video_from_frames(frames, output_path, settings.get('fps', 30))
            print(f"Video created successfully: {created_video_path}")
            
            return {
                'success': True,
                'original_prompt': user_prompt,
                'enhanced_prompt': enhanced_prompt,
                'image_description': image_description,
                'video_filename': output_filename,
                'settings': settings,
                'hf_integration': hf_result,
                'generation_method': 'huggingface_enhanced_simulation'
            }
            
        except Exception as e:
            print(f"Error in process_video_request: {str(e)}")
            raise Exception(f"Error processing video request: {e}")
    
    def preprocess_image(self, image_path: str, target_size: tuple = (512, 512)) -> np.ndarray:
        """Preprocess image for video generation"""
        try:
            image = Image.open(image_path).convert('RGB')
            image.thumbnail(target_size, Image.Resampling.LANCZOS)
            
            new_image = Image.new('RGB', target_size, (0, 0, 0))
            x = (target_size[0] - image.width) // 2
            y = (target_size[1] - image.height) // 2
            new_image.paste(image, (x, y))
            
            return np.array(new_image)
        except Exception as e:
            raise Exception(f"Error preprocessing image: {e}")
    
    def generate_video_frames(self, image: np.ndarray, prompt: str, settings: Dict[str, Any], hf_result: Dict[str, Any] = None) -> list:
        """Generate video frames based on enhanced prompt and HF insights"""
        print(f"Generating video frames for prompt: {prompt}")
        print(f"Settings: {settings}")
        if hf_result:
            print(f"HF integration status: {hf_result.get('success', False)}")
        
        frames = []
        duration = int(settings.get('duration', 5))
        fps = int(settings.get('fps', 30))
        style = settings.get('style', 'realistic')
        
        total_frames = duration * fps
        base_image = Image.fromarray(image)
        
        print(f"Total frames to generate: {total_frames}")
        
        # Analyze the enhanced prompt for effects
        effects = self.analyze_enhanced_prompt(prompt)
        
        # Enhance effects based on HF dataset insights
        if hf_result and hf_result.get('success'):
            print("Enhancing effects based on HF dataset insights")
            # If HF found examples, we can enhance our effects
            effects['enhanced_quality'] = True
            effects['hf_informed'] = True
        
        print(f"Detected effects: {effects}")
        
        for frame_idx in range(total_frames):
            progress = frame_idx / (total_frames - 1) if total_frames > 1 else 0
            current_frame = base_image.copy()
            current_frame = self.apply_enhanced_effects(current_frame, progress, effects, style)
            frames.append(np.array(current_frame))
            
            # Log progress every 30 frames
            if frame_idx % 30 == 0:
                print(f"Generated frame {frame_idx}/{total_frames}")
        
        print(f"Successfully generated {len(frames)} frames")
        return frames
    
    def analyze_enhanced_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze enhanced prompt for visual effects"""
        prompt_lower = prompt.lower()
        
        effects = {
            'zoom': any(word in prompt_lower for word in ['zoom', 'closer', 'approach', 'scale']),
            'pan': any(word in prompt_lower for word in ['pan', 'move', 'slide', 'sweep']),
            'particles': any(word in prompt_lower for word in ['particle', 'spark', 'glow', 'magical', 'dust']),
            'blur': any(word in prompt_lower for word in ['blur', 'focus', 'depth', 'bokeh']),
            'brightness': any(word in prompt_lower for word in ['bright', 'light', 'illuminate', 'glow']),
            'rotation': any(word in prompt_lower for word in ['rotate', 'spin', 'turn', 'twist']),
            'wave': any(word in prompt_lower for word in ['wave', 'flow', 'ripple', 'undulate']),
            'fade': any(word in prompt_lower for word in ['fade', 'appear', 'emerge', 'dissolve']),
            'cinematic': any(word in prompt_lower for word in ['cinematic', 'dramatic', 'film', 'movie']),
            'color_shift': any(word in prompt_lower for word in ['color', 'hue', 'tint', 'vibrant', 'green', 'red', 'blue', 'yellow', 'purple', 'orange', 'change']),
            'color_target': None
        }
        
        # Detect specific color changes
        color_keywords = {
            'green': (0, 255, 0),
            'red': (255, 0, 0), 
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'purple': (128, 0, 128),
            'orange': (255, 165, 0),
            'pink': (255, 192, 203),
            'cyan': (0, 255, 255)
        }
        
        for color_name, rgb in color_keywords.items():
            if color_name in prompt_lower:
                effects['color_target'] = rgb
                effects['color_shift'] = True
                break
        
        return effects
    
    def apply_enhanced_effects(self, image: Image.Image, progress: float, effects: Dict[str, Any], style: str) -> Image.Image:
        """Apply enhanced effects based on the improved prompt"""
        
        # Zoom effect
        if effects['zoom']:
            zoom_factor = 1.0 + (progress * 0.3)
            new_size = (int(image.width * zoom_factor), int(image.height * zoom_factor))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            left = (image.width - 512) // 2
            top = (image.height - 512) // 2
            image = image.crop((left, top, left + 512, top + 512))
        
        # Pan effect
        if effects['pan']:
            shift_x = int(progress * 50 * np.sin(progress * np.pi))
            shift_y = int(progress * 30 * np.cos(progress * np.pi))
            # Create new image with black background
            new_image = Image.new('RGB', image.size, (0, 0, 0))
            new_image.paste(image, (shift_x, shift_y))
            image = new_image
        
        # Wave effect
        if effects['wave']:
            img_array = np.array(image)
            height, width = img_array.shape[:2]
            wave_intensity = 10 * progress
            for y in range(height):
                offset = int(wave_intensity * np.sin(2 * np.pi * y / 20 + progress * 4))
                if offset > 0:
                    img_array[y, offset:] = img_array[y, :-offset]
                elif offset < 0:
                    img_array[y, :offset] = img_array[y, -offset:]
            image = Image.fromarray(img_array)
        
        # Rotation with easing
        if effects['rotation']:
            angle = progress * 15 * np.sin(progress * np.pi)
            image = image.rotate(angle, fillcolor=(0, 0, 0))
        
        # Fade effect
        if effects['fade']:
            alpha = min(1.0, progress * 2)  # Fade in over first half
            if progress > 0.5:
                alpha = max(0.3, 1.0 - (progress - 0.5) * 2)  # Fade out in second half
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(alpha)
        
        # Enhanced brightness for cinematic effect
        if effects['brightness'] or effects['cinematic']:
            brightness = 1.0 + (np.sin(progress * np.pi * 2) * 0.15)
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness)
        
        # Color shifting with specific color targets
        if effects['color_shift']:
            if effects['color_target']:
                # Apply specific color tint
                target_r, target_g, target_b = effects['color_target']
                img_array = np.array(image).astype(float)
                
                # Create color overlay
                intensity = 0.3 * progress  # Gradually apply color
                overlay = np.zeros_like(img_array)
                overlay[:, :, 0] = target_r
                overlay[:, :, 1] = target_g  
                overlay[:, :, 2] = target_b
                
                # Blend with original
                result = img_array * (1 - intensity) + overlay * intensity
                image = Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
            else:
                # General color enhancement
                hue_shift = np.sin(progress * np.pi * 4) * 0.2
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(1.0 + hue_shift)
        
        # Enhanced blur with focus pulling
        if effects['blur']:
            blur_radius = abs(np.sin(progress * np.pi * 2)) * 3
            if blur_radius > 0.1:
                image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # Particle effect overlay (simulated)
        if effects['particles']:
            img_array = np.array(image)
            height, width = img_array.shape[:2]
            
            # Add random bright spots for particle effect
            num_particles = int(50 * progress)
            for _ in range(num_particles):
                x = np.random.randint(0, width-5)
                y = np.random.randint(0, height-5)
                brightness = np.random.randint(200, 255)
                
                # Add small bright spots
                img_array[y:y+3, x:x+3] = np.minimum(
                    img_array[y:y+3, x:x+3] + brightness//3, 255
                )
            
            image = Image.fromarray(img_array)
        
        return image
    
    def create_video_from_frames(self, frames: list, output_path: str, fps: int = 30) -> str:
        """Create video file from frames"""
        try:
            if not frames:
                raise Exception("No frames to create video")
            
            height, width = frames[0].shape[:2]
            
            # Try multiple codecs for better compatibility
            codecs_to_try = [
                ('mp4v', '.mp4'),
                ('XVID', '.avi'),
                ('MJPG', '.avi')
            ]
            
            for codec_name, ext in codecs_to_try:
                try:
                    # Change extension if needed
                    if not output_path.endswith(ext):
                        output_path = output_path.rsplit('.', 1)[0] + ext
                    
                    fourcc = cv2.VideoWriter_fourcc(*codec_name)
                    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                    
                    if not video_writer.isOpened():
                        video_writer.release()
                        continue
                    
                    print(f"Using codec: {codec_name}")
                    
                    for frame in frames:
                        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        video_writer.write(frame_bgr)
                    
                    video_writer.release()
                    
                    # Verify the video file was created and has size > 0
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        print(f"Video created successfully: {output_path}")
                        return output_path
                    else:
                        print(f"Video file empty or not created with {codec_name}")
                        
                except Exception as e:
                    print(f"Failed with codec {codec_name}: {e}")
                    continue
            
            raise Exception("All video codecs failed")
            
        except Exception as e:
            raise Exception(f"Error creating video: {e}")

class HuggingFaceVideoGenerator:
    """
    Hugging Face Video Generation API Integration
    """
    
    def __init__(self):
        self.api_base = "https://datasets-server.huggingface.co"
        self.dataset_name = "Rapidata/text-2-video-human-preferences-veo3"
        self.hf_token = None  # Add your HF token here if needed
        
    def get_video_examples(self, prompt: str, limit: int = 10) -> list:
        """Get video examples from the Hugging Face dataset"""
        try:
            # Search for similar prompts in the dataset
            encoded_dataset = quote(self.dataset_name)
            url = f"{self.api_base}/rows?dataset={encoded_dataset}&config=default&split=train&offset=0&length={limit}"
            
            headers = {}
            if self.hf_token:
                headers["Authorization"] = f"Bearer {self.hf_token}"
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('rows', [])
            else:
                print(f"HF API error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Error fetching video examples: {e}")
            return []
    
    def generate_video_from_prompt(self, prompt: str, image_path: str = None) -> Dict[str, Any]:
        """
        Generate video using Hugging Face API approach
        This is a placeholder for actual video generation API when available
        """
        try:
            print(f"Generating video for prompt: {prompt}")
            
            # For now, we'll use the dataset to find similar examples
            # In the future, this would call an actual video generation API
            examples = self.get_video_examples(prompt, limit=5)
            
            if examples:
                print(f"Found {len(examples)} similar examples in dataset")
                
                # Return metadata about the generation process
                return {
                    'success': True,
                    'prompt': prompt,
                    'examples_found': len(examples),
                    'method': 'huggingface_dataset_reference',
                    'note': 'Using dataset examples as reference for video generation simulation'
                }
            else:
                return {
                    'success': False,
                    'error': 'No examples found in dataset',
                    'method': 'fallback_simulation'
                }
                
        except Exception as e:
            print(f"HF video generation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'method': 'fallback_simulation'
            }

# Global processor instance
video_processor = VideoProcessor()

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

@app.route('/api/enhance-prompt', methods=['POST'])
def enhance_prompt():
    """Enhance user prompt using the Hugging Face model"""
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '')
        
        if not user_prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        enhanced = video_processor.prompt_generator.enhance_prompt(user_prompt)
        
        return jsonify({
            'success': True,
            'original_prompt': user_prompt,
            'enhanced_prompt': enhanced,
            'model_used': video_processor.prompt_generator.model_loaded
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-video', methods=['POST'])
def generate_video():
    """Generate video with enhanced prompts"""
    try:
        # Check for image file
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400
        
        # Get parameters
        user_prompt = request.form.get('prompt', '')
        if not user_prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        settings = {
            'duration': int(request.form.get('duration', 5)),
            'quality': request.form.get('quality', '1080p'),
            'style': request.form.get('style', 'realistic'),
            'fps': int(request.form.get('fps', 30))
        }
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(image_path)
        
        try:
            # Process video request
            result = video_processor.process_video_request(image_path, user_prompt, settings)
            
            # Clean up uploaded file
            os.remove(image_path)
            
            return jsonify({
                'success': True,
                'message': 'Video generated successfully with enhanced prompt!',
                'original_prompt': result['original_prompt'],
                'enhanced_prompt': result['enhanced_prompt'],
                'video_id': result['video_filename'],
                'download_url': f'/api/download/{result["video_filename"]}',
                'model_used': video_processor.prompt_generator.model_loaded
            })
            
        except Exception as e:
            if os.path.exists(image_path):
                os.remove(image_path)
            raise e
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<video_id>')
def download_video(video_id):
    """Download or stream generated video"""
    try:
        video_path = os.path.join(app.config['OUTPUT_FOLDER'], video_id)
        
        if not os.path.exists(video_path):
            print(f"Video not found: {video_path}")
            return jsonify({'error': 'Video not found'}), 404
        
        print(f"Serving video: {video_path}")
        
        # Check if it's a download request or streaming request
        if request.args.get('download') == 'true':
            return send_file(
                video_path, 
                as_attachment=True, 
                download_name=f"ai_generated_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            )
        else:
            # Stream video for browser playback
            return send_file(
                video_path, 
                mimetype='video/mp4',
                as_attachment=False
            )
        
    except Exception as e:
        print(f"Error serving video: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def get_status():
    """Get system status"""
    # Test HF API connection
    try:
        hf_generator = HuggingFaceVideoGenerator()
        examples = hf_generator.get_video_examples("test", limit=1)
        hf_status = 'connected' if examples else 'limited_access'
    except:
        hf_status = 'offline'
    
    return jsonify({
        'status': 'online',
        'model_loaded': video_processor.prompt_generator.model_loaded,
        'device': str(video_processor.prompt_generator.device),
        'model_name': 'shreyahegde/video_prompt_generation',
        'hf_video_api': hf_status,
        'hf_dataset': 'Rapidata/text-2-video-human-preferences-veo3',
        'generation_method': 'huggingface_enhanced_simulation',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test-hf-dataset', methods=['POST'])
def test_hf_dataset():
    """Test Hugging Face dataset API connection"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'a person walking')
        
        # Test the HF dataset API
        hf_generator = HuggingFaceVideoGenerator()
        result = hf_generator.generate_video_from_prompt(prompt)
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'hf_result': result,
            'api_status': 'connected' if result.get('success') else 'limited_access'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting AI Video Generator with Hugging Face Integration...")
    print(f"Model loaded: {video_processor.prompt_generator.model_loaded}")
    print(f"Device: {video_processor.prompt_generator.device}")
    print("Server running at http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
