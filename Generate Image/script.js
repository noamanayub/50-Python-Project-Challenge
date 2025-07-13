class VideoGenerator {
    constructor() {
        this.selectedImage = null;
        this.isGenerating = false;
        this.initializeElements();
        this.bindEvents();
        this.initializeAnimations();
        this.checkAPIStatus(); // Check API status on page load
    }

    initializeElements() {
        // Upload elements
        this.uploadArea = document.getElementById('uploadArea');
        this.imageInput = document.getElementById('imageInput');
        this.imagePreview = document.getElementById('imagePreview');
        this.previewImg = document.getElementById('previewImg');
        this.imageName = document.getElementById('imageName');
        this.removeImage = document.getElementById('removeImage');

        // Prompt elements
        this.promptInput = document.getElementById('promptInput');
        this.charCount = document.getElementById('charCount');
        this.suggestionTags = document.querySelectorAll('.suggestion-tag');

        // Settings elements
        this.duration = document.getElementById('duration');
        this.quality = document.getElementById('quality');
        this.style = document.getElementById('style');
        this.fps = document.getElementById('fps');

        // Generation elements
        this.generateBtn = document.getElementById('generateBtn');
        this.btnContent = this.generateBtn.querySelector('.btn-content');
        this.btnLoader = this.generateBtn.querySelector('.btn-loader');

        // Progress elements
        this.progressSection = document.getElementById('progressSection');
        this.progressFill = document.getElementById('progressFill');
        this.progressText = document.getElementById('progressText');
        this.progressPercent = document.getElementById('progressPercent');
        this.steps = {
            step1: document.getElementById('step1'),
            step2: document.getElementById('step2'),
            step3: document.getElementById('step3'),
            step4: document.getElementById('step4')
        };

        // Result elements
        this.resultSection = document.getElementById('resultSection');
        this.resultVideo = document.getElementById('resultVideo');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.shareBtn = document.getElementById('shareBtn');
        this.newVideoBtn = document.getElementById('newVideoBtn');
        
        // Enhanced prompt elements
        this.enhancedPromptSection = document.getElementById('enhancedPromptSection');
        this.originalPromptText = document.getElementById('originalPromptText');
        this.enhancedPromptText = document.getElementById('enhancedPromptText');

        // Status
        this.statusIndicator = document.querySelector('.status-indicator span');
        this.statusDot = document.querySelector('.status-dot');
        this.shareBtn = document.getElementById('shareBtn');
        this.newVideoBtn = document.getElementById('newVideoBtn');

        // Status indicator
        this.statusIndicator = document.querySelector('.status-indicator span');
    }

    bindEvents() {
        // Upload events
        this.uploadArea.addEventListener('click', () => this.imageInput.click());
        this.uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        this.uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
        this.uploadArea.addEventListener('drop', this.handleDrop.bind(this));
        this.imageInput.addEventListener('change', this.handleImageSelect.bind(this));
        this.removeImage.addEventListener('click', this.removeSelectedImage.bind(this));

        // Prompt events
        this.promptInput.addEventListener('input', this.updateCharCount.bind(this));
        this.suggestionTags.forEach(tag => {
            tag.addEventListener('click', () => this.applySuggestion(tag));
        });

        // Generation events
        this.generateBtn.addEventListener('click', this.generateVideo.bind(this));

        // Result events
        this.downloadBtn.addEventListener('click', this.downloadVideo.bind(this));
        this.shareBtn.addEventListener('click', this.shareVideo.bind(this));
        this.newVideoBtn.addEventListener('click', this.startNew.bind(this));

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            document.addEventListener(eventName, e => e.preventDefault());
        });
    }

    initializeAnimations() {
        // Add entrance animations to sections
        const sections = document.querySelectorAll('.upload-section, .prompt-section, .settings-section, .generate-section');
        sections.forEach((section, index) => {
            section.style.opacity = '0';
            section.style.transform = 'translateY(30px)';
            setTimeout(() => {
                section.style.transition = 'all 0.6s ease';
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }

    // Image Upload Methods
    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processImageFile(files[0]);
        }
    }

    handleImageSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processImageFile(file);
        }
    }

    processImageFile(file) {
        if (!this.isValidImageFile(file)) {
            this.showNotification('Please select a valid image file (JPG, PNG, GIF, WebP)', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            this.selectedImage = file;
            this.previewImg.src = e.target.result;
            this.imageName.textContent = file.name;
            this.showImagePreview();
            this.updateStatus('Image loaded');
            this.validateForm();
        };
        reader.readAsDataURL(file);
    }

    isValidImageFile(file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        return validTypes.includes(file.type);
    }

    showImagePreview() {
        this.uploadArea.style.display = 'none';
        this.imagePreview.style.display = 'block';
        this.imagePreview.style.animation = 'slideInUp 0.5s ease';
    }

    removeSelectedImage() {
        this.selectedImage = null;
        this.imageInput.value = '';
        this.uploadArea.style.display = 'block';
        this.imagePreview.style.display = 'none';
        this.updateStatus('Ready');
        this.validateForm();
    }

    // Prompt Methods
    updateCharCount() {
        const count = this.promptInput.value.length;
        this.charCount.textContent = count;
        
        if (count > 400) {
            this.charCount.style.color = 'var(--secondary-color)';
        } else {
            this.charCount.style.color = 'var(--text-light)';
        }
        
        this.validateForm();
    }

    applySuggestion(tag) {
        const prompt = tag.dataset.prompt;
        this.promptInput.value = prompt;
        this.updateCharCount();
        
        // Add visual feedback
        tag.style.transform = 'scale(0.95)';
        setTimeout(() => {
            tag.style.transform = '';
        }, 150);
    }

    // Validation
    validateForm() {
        const hasImage = this.selectedImage !== null;
        const hasPrompt = this.promptInput.value.trim().length > 0;
        const isValid = hasImage && hasPrompt && !this.isGenerating;
        
        this.generateBtn.disabled = !isValid;
        this.generateBtn.style.opacity = isValid ? '1' : '0.6';
        this.generateBtn.style.cursor = isValid ? 'pointer' : 'not-allowed';
    }

    // Video Generation
    async generateVideo() {
        if (!this.selectedImage || !this.promptInput.value.trim()) {
            this.showNotification('Please select an image and enter a prompt', 'error');
            return;
        }

        this.isGenerating = true;
        this.showGenerationUI();
        
        try {
            // Check backend status first
            console.log('Checking backend status...');
            const statusCheck = await this.checkAPIStatus();
            console.log('Backend status:', statusCheck);
            
            // First enhance the prompt using Hugging Face model
            const originalPrompt = this.promptInput.value.trim();
            console.log('Original prompt:', originalPrompt);
            
            const enhancedPrompt = await this.enhancePrompt(originalPrompt);
            console.log('Enhanced prompt:', enhancedPrompt);
            
            // Show enhanced prompt comparison
            if (enhancedPrompt && enhancedPrompt !== originalPrompt) {
                this.showEnhancedPrompt(originalPrompt, enhancedPrompt);
            }
            
            // Call the backend API for video generation
            console.log('Calling video generation API...');
            const result = await this.callVideoGenerationAPI();
            console.log('API result:', result);
            
            if (result.success) {
                console.log('Video generation result:', result);
                this.showResult(result);
                this.showNotification('Video generated successfully!', 'success');
            } else {
                throw new Error(result.error || 'Failed to generate video');
            }
            
        } catch (error) {
            console.error('Error generating video:', error);
            
            // Check if it's a network error (backend not running)
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                this.showNotification('⚠️ Backend server is not running. Please start the Flask server first!', 'error');
                this.showServerInstructions();
            } else {
                this.showNotification(`Error: ${error.message}`, 'error');
            }
            
        } finally {
            this.isGenerating = false;
            this.btnContent.style.display = 'flex';
            this.btnLoader.style.display = 'none';
            this.generateBtn.disabled = false;
            this.validateForm();
        }
    }

    showGenerationUI() {
        this.btnContent.style.display = 'none';
        this.btnLoader.style.display = 'flex';
        this.generateBtn.disabled = true;
        
        this.progressSection.style.display = 'block';
        this.progressSection.style.animation = 'slideInUp 0.5s ease';
        this.resultSection.style.display = 'none';
        
        this.updateStatus('Generating video...');
        
        // Reset progress
        this.progressFill.style.width = '0%';
        this.progressPercent.textContent = '0%';
        Object.values(this.steps).forEach(step => {
            step.classList.remove('active', 'completed');
        });
    }

    async simulateVideoGeneration() {
        const steps = [
            { step: 'step1', text: 'Analyzing image...', duration: 2000 },
            { step: 'step2', text: 'Processing prompt...', duration: 1500 },
            { step: 'step3', text: 'Generating frames...', duration: 3000 },
            { step: 'step4', text: 'Rendering video...', duration: 2500 }
        ];

        let totalProgress = 0;
        const progressPerStep = 100 / steps.length;

        for (let i = 0; i < steps.length; i++) {
            const step = steps[i];
            
            // Mark current step as active
            this.steps[step.step].classList.add('active');
            this.progressText.textContent = step.text;
            
            // Animate progress
            const startProgress = totalProgress;
            const endProgress = totalProgress + progressPerStep;
            
            await this.animateProgress(startProgress, endProgress, step.duration);
            
            // Mark step as completed
            this.steps[step.step].classList.remove('active');
            this.steps[step.step].classList.add('completed');
            
            totalProgress = endProgress;
        }
    }

    animateProgress(start, end, duration) {
        return new Promise(resolve => {
            const startTime = Date.now();
            const animate = () => {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const currentProgress = start + (end - start) * progress;
                
                this.progressFill.style.width = `${currentProgress}%`;
                this.progressPercent.textContent = `${Math.round(currentProgress)}%`;
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    resolve();
                }
            };
            animate();
        });
    }

    createSampleVideo() {
        // Create a canvas-based video simulation
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');
        
        // Draw the uploaded image on canvas with animation effect
        const img = new Image();
        img.onload = () => {
            // Create a simple animation by drawing the image with effects
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            
            // Convert to blob and create video URL
            canvas.toBlob((blob) => {
                const url = URL.createObjectURL(blob);
                // For demo purposes, we'll use a sample video URL
                // In a real implementation, you would generate actual video frames
                this.resultVideo.src = "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4";
                this.resultVideo.poster = canvas.toDataURL();
            });
        };
        img.src = this.previewImg.src;
    }

    showResult(apiResult = null) {
        this.progressSection.style.display = 'none';
        this.resultSection.style.display = 'block';
        this.resultSection.style.animation = 'slideInUp 0.5s ease';
        
        const video = this.resultVideo;
        const overlay = document.getElementById('videoLoadingOverlay');
        
        // Set video source if apiResult is provided
        if (apiResult && apiResult.download_url) {
            console.log('Setting video source:', apiResult.download_url);
            
            // Clear any previous video source
            video.src = '';
            video.load();
            
            // Set new video source
            video.src = apiResult.download_url;
            
            if (overlay) overlay.style.display = 'flex';
            
            // Add timeout for video loading
            const loadTimeout = setTimeout(() => {
                if (overlay) overlay.style.display = 'none';
                this.showNotification('Video loading timeout. Try refreshing.', 'warning');
            }, 10000);
            
            video.oncanplay = () => {
                console.log('Video can play');
                clearTimeout(loadTimeout);
                if (overlay) overlay.style.display = 'none';
            };
            
            video.onloadeddata = () => {
                console.log('Video data loaded');
                clearTimeout(loadTimeout);
                if (overlay) overlay.style.display = 'none';
            };
            
            video.onerror = (e) => {
                console.error('Video error:', e);
                clearTimeout(loadTimeout);
                if (overlay) overlay.style.display = 'none';
                this.showNotification('Video failed to load. Check server logs.', 'error');
            };
            
            video.load();
            
            // Update download button
            if (this.downloadBtn) {
                this.downloadBtn.onclick = () => {
                    window.open(apiResult.download_url + '?download=true', '_blank');
                };
            }
        } else {
            // Hide overlay if no video
            if (overlay) overlay.style.display = 'none';
        }
        
        this.btnContent.style.display = 'flex';
        this.btnLoader.style.display = 'none';
        this.generateBtn.disabled = false;
    }

    displayEnhancedPromptInfo(result) {
        // Create enhanced prompt display if it doesn't exist
        let promptInfo = document.getElementById('promptInfo');
        if (!promptInfo) {
            promptInfo = document.createElement('div');
            promptInfo.id = 'promptInfo';
            promptInfo.className = 'prompt-info';
            this.resultSection.querySelector('.result-card').insertBefore(
                promptInfo, 
                this.resultSection.querySelector('.video-container')
            );
        }

        promptInfo.innerHTML = `
            <h4>AI Enhanced Prompt</h4>
            <div class="prompt-comparison">
                <div class="original-prompt">
                    <strong>Original:</strong> ${result.original_prompt}
                </div>
                <div class="enhanced-prompt">
                    <strong>Enhanced:</strong> ${result.enhanced_prompt}
                </div>
            </div>
            <div class="model-info">
                <small>Generated using: ${result.model_used ? 'Hugging Face Model' : 'Fallback Enhancement'}</small>
            </div>
        `;
    }

    // Result Actions
    downloadVideo() {
        if (this.resultVideo.src) {
            const link = document.createElement('a');
            link.href = this.resultVideo.src;
            link.download = `generated_video_${Date.now()}.mp4`;
            link.click();
            this.showNotification('Video download started!', 'success');
        } else {
            this.showNotification('No video available to download', 'error');
        }
    }

    shareVideo() {
        if (navigator.share) {
            navigator.share({
                title: 'AI Generated Video',
                text: 'Check out this amazing video I created with AI!',
                url: window.location.href
            });
        } else {
            // Fallback for browsers that don't support Web Share API
            navigator.clipboard.writeText(window.location.href);
            this.showNotification('Link copied to clipboard!', 'success');
        }
    }

    startNew() {
        this.removeSelectedImage();
        this.promptInput.value = '';
        this.updateCharCount();
        this.progressSection.style.display = 'none';
        this.resultSection.style.display = 'none';
        this.updateStatus('Ready');
        
        // Reset progress
        this.progressFill.style.width = '0%';
        this.progressPercent.textContent = '0%';
        Object.values(this.steps).forEach(step => {
            step.classList.remove('active', 'completed');
        });
        
        if (this.enhancedPromptSection) {
            this.enhancedPromptSection.style.display = 'none';
        }
        
        this.showNotification('Ready for a new video!', 'info');
    }

    // Utility Methods
    updateStatus(message, type = 'default') {
        this.statusIndicator.textContent = message;
        this.statusDot.className = 'status-dot';
        
        if (type === 'success') {
            this.statusDot.classList.add('success');
        } else if (type === 'warning') {
            this.statusDot.classList.add('warning');
        } else if (type === 'error') {
            this.statusDot.classList.add('error');
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '15px 20px',
            borderRadius: '12px',
            color: 'white',
            fontWeight: '500',
            zIndex: '10000',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease',
            maxWidth: '300px',
            wordWrap: 'break-word'
        });

        // Set background color based on type
        switch (type) {
            case 'success':
                notification.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                break;
            case 'error':
                notification.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
                break;
            case 'info':
                notification.style.background = 'linear-gradient(135deg, #3b82f6, #2563eb)';
                break;
            default:
                notification.style.background = 'linear-gradient(135deg, #6366f1, #4f46e5)';
        }

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remove after delay
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // API Methods - Hugging Face Integration
    async enhancePrompt(userPrompt) {
        try {
            const response = await fetch('/api/enhance-prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: userPrompt })
            });

            if (!response.ok) {
                throw new Error('Failed to enhance prompt');
            }

            const result = await response.json();
            return result.enhanced_prompt;
        } catch (error) {
            console.error('Error enhancing prompt:', error);
            return userPrompt; // Return original if enhancement fails
        }
    }

    async callVideoGenerationAPI() {
        const formData = new FormData();
        formData.append('image', this.selectedImage);
        formData.append('prompt', this.promptInput.value);
        formData.append('duration', this.duration.value);
        formData.append('quality', this.quality.value);
        formData.append('style', this.style.value);
        formData.append('fps', this.fps.value);

        const response = await fetch('/api/generate-video', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to generate video');
        }

        return await response.json();
    }

    showServerInstructions() {
        // Create instruction modal
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
        `;
        
        const content = document.createElement('div');
        content.style.cssText = `
            background: white;
            border-radius: 20px;
            padding: 30px;
            max-width: 500px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        `;
        
        content.innerHTML = `
            <h3 style="color: #1f2937; margin-bottom: 20px;">🚀 Start the Backend Server</h3>
            <p style="color: #6b7280; margin-bottom: 20px;">
                To use the AI features, you need to start the Flask backend server first.
            </p>
            <div style="background: #f3f4f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <strong>Open a terminal and run:</strong><br>
                <code style="color: #dc2626; font-size: 1.1em;">python app.py</code>
            </div>
            <p style="color: #9ca3af; font-size: 0.9em; margin-bottom: 20px;">
                Then refresh this page to use the AI-enhanced video generation!
            </p>
            <button id="closeModal" style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                cursor: pointer;
                font-weight: 600;
            ">Got it!</button>
        `;
        
        modal.appendChild(content);
        document.body.appendChild(modal);
        
        // Close modal on click
        document.getElementById('closeModal').onclick = () => {
            document.body.removeChild(modal);
        };
        
        modal.onclick = (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        };
    }

    // Check backend status on page load
    async checkBackendStatus() {
        try {
            const response = await fetch('/api/status', { timeout: 3000 });
            if (response.ok) {
                const data = await response.json();
                this.updateBackendStatus(true, data);
                return true;
            }
        } catch (error) {
            this.updateBackendStatus(false);
            return false;
        }
    }

    updateBackendStatus(isOnline, data = null) {
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-indicator span');
        
        if (isOnline && data) {
            statusDot.style.background = '#10b981'; // Green
            statusText.textContent = data.model_loaded ? 'AI Model Ready' : 'Backend Online';
            this.showNotification('🤖 AI backend is ready!', 'success');
        } else {
            statusDot.style.background = '#ef4444'; // Red
            statusText.textContent = 'Backend Offline';
        }
    }

    async checkAPIStatus() {
        try {
            const response = await fetch('/api/status');
            const result = await response.json();
            
            if (result.model_loaded) {
                this.updateStatus('AI Model Ready', 'success');
            } else {
                this.updateStatus('Simulation Mode', 'warning');
            }
            
            return result;
        } catch (error) {
            console.error('API status check failed:', error);
            this.updateStatus('Server Offline', 'error');
            return { status: 'offline', model_loaded: false };
        }
    }

    showEnhancedPrompt(originalPrompt, enhancedPrompt) {
        this.originalPromptText.textContent = originalPrompt;
        this.enhancedPromptText.textContent = enhancedPrompt;
        
        this.enhancedPromptSection.style.display = 'block';
        this.enhancedPromptSection.style.animation = 'slideInUp 0.5s ease';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    const app = new VideoGenerator();
    
    // Check if backend is running
    const backendOnline = await app.checkBackendStatus();
    
    if (!backendOnline) {
        // Show instructions after a delay
        setTimeout(() => {
            app.showNotification('💡 For AI features, start the backend server', 'info');
        }, 2000);
    }
    
    // Simple loading animation
    const body = document.body;
    body.style.opacity = '0';
    body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        body.style.opacity = '1';
    }, 100);
    
    console.log('AI Video Generator initialized successfully!');
});
