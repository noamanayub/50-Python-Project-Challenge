# CipherChat - Modern Web Messaging App

A stunning WhatsApp-like messaging application built with Flask, HTML, CSS, and JavaScript, featuring a beautiful 3D UI design with blue color theme, real-time messaging, and advanced message management capabilities.

## 🌟 Features

### Modern 3D Web Interface
- **Stunning 3D Design**: Beautiful gradients, shadows, and hover effects throughout
- **Real-time Messaging**: Instant messaging with WebSocket support
- **Premium Visual Effects**: Smooth animations, transitions, and interactive elements
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Blue Color Theme**: Beautiful blue gradient theme (#55A2CC and #255A94)

### Advanced Message Management
- **Message Selection**: Click to select individual messages
- **Bulk Actions**: Select multiple messages for bulk operations
- **Per-Message Delete**: Delete specific messages with hover actions
- **Bulk Delete**: Delete multiple selected messages at once
- **Real-time Updates**: All users see deletions instantly
- **Message Actions**: Hover over messages to see action buttons

### Enhanced User Experience
- **Logo Integration**: Your logo.png displayed prominently in the white navbar
- **High-Quality Stickers**: 20 custom stickers (optimized size: 120px max)
- **Typing Indicators**: See when contacts are typing
- **Message Timestamps**: All messages show delivery time
- **Auto-Reply System**: Contacts automatically respond to keep conversations alive
- **Toast Notifications**: Beautiful notifications for system events
- **Visual Feedback**: Smooth animations for all interactions

### Technical Features
- **Real-time Communication**: WebSocket-based instant messaging
- **Message Persistence**: All conversations saved automatically with unique IDs
- **Multiple Contacts**: Chat with Alice, Bob, Charlie, Diana, and Eve
- **Sticker Support**: Send high-quality stickers seamlessly
- **Modern Web Technologies**: HTML5, CSS3, JavaScript ES6+, Flask, Socket.IO
- **Message ID System**: Each message has a unique identifier for management

## 🚀 Installation

1. **Install Python 3.8+**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

3. **Start chatting:**
3. **Start chatting:**
   - Click on any contact in the left sidebar
   - Type messages in the input area
   - Press Enter to send or click the send button
   - Click the sticker button to send stickers
   - Hover over messages to see action buttons (select/delete)
   - Select multiple messages for bulk operations
   - Use the bulk actions bar to delete selected messages
   - Enjoy the 3D interface and smooth animations!

## 🎨 Design Features

### 3D Visual Elements
- **Gradient Backgrounds**: Beautiful blue gradients throughout the interface
- **Box Shadows**: Realistic depth and dimension
- **Hover Effects**: Interactive buttons with smooth transitions
- **Animated Elements**: Smooth animations for messages and UI interactions
- **Glass Morphism**: Modern transparent effects
- **Message Actions**: Elegant hover buttons for message management

### Color Theme Integration
- **Primary Color**: #55A2CC (Light Blue) - Used for main elements
- **Secondary Color**: #255A94 (Dark Blue) - Used for accents
- **Accent Color**: #4A90E2 (Premium Blue) - Used for highlights
- **Message Colors**: Blue for sent messages, white for received
- **Consistent Theming**: All elements follow the blue color scheme
- **White Navbar**: Clean white background with blue accents

### Typography and Layout
- **Modern Fonts**: Clean, readable typography
- **Responsive Grid**: Flexible layout that adapts to screen size
- **Proper Spacing**: Consistent margins and padding
- **Visual Hierarchy**: Clear information structure

## 📱 Interface Components

### Header/Navbar
- **Logo Display**: Your logo.png prominently featured (60px, larger size)
- **App Title**: "CipherChat" with custom blue gradient styling
- **Status Indicator**: Online status with pulsing animation
- **Real-time Clock**: Current time display
- **Clean White Background**: Professional white navbar with blue accents

### Sidebar
- **Contact List**: All contacts with avatars and status
- **Active State**: Visual indication of selected contact
- **Hover Effects**: Smooth transitions on interaction
- **Online Indicators**: Status indicators for each contact
- **Blue Gradient Background**: Elegant dark blue gradient

### Chat Area
- **Message Bubbles**: 3D styled message containers with blue theme
- **Sticker Integration**: Optimized sticker display (120px max size)
- **Typing Indicators**: Animated typing notifications
- **Timestamp Display**: Message delivery times
- **Smooth Scrolling**: Auto-scroll to latest messages
- **Message Actions**: Hover buttons for select and delete
- **Selection Highlights**: Visual feedback for selected messages

### Input Area
- **Auto-resizing Textarea**: Grows with message length
- **Send Button**: Animated send functionality with blue gradients
- **Sticker Button**: Easy access to sticker picker
- **Visual Feedback**: Confirmation animations
- **Blue Theme**: Consistent blue color scheme throughout

### Message Management
- **Individual Selection**: Click select button to choose messages
- **Bulk Actions Bar**: Appears when messages are selected
- **Delete Options**: Per-message and bulk delete functionality
- **Real-time Updates**: All users see changes instantly
- **Visual Feedback**: Smooth animations for all operations

## 🔧 Technical Architecture

### Backend (Flask)
```
app.py                 # Main Flask application
├── Routes
│   ├── / (home)      # Main chat interface
│   ├── /api/messages # Message retrieval
│   ├── /api/send_message # Message sending
│   ├── /api/stickers # Sticker data
│   ├── /api/clear_chat # Clear chat history
│   └── /api/delete_messages # Delete specific messages
├── WebSocket Events
│   ├── connect/disconnect
│   ├── join_chat/leave_chat
│   ├── new_message
│   ├── user_typing
│   ├── messages_deleted # Broadcast message deletions
│   └── chat_cleared # Broadcast chat clearing
└── Auto-reply System
```

### Frontend Structure
```
templates/
└── index.html         # Main HTML template

static/
├── css/
│   └── style.css      # 3D styling and animations
├── js/
│   └── app.js         # JavaScript functionality
├── stickers/          # Sticker images (1.png - 20.png)
└── logo.png          # Your logo file
```

### Key Technologies
- **Flask**: Python web framework
- **Socket.IO**: Real-time bidirectional communication
- **HTML5**: Modern markup structure
- **CSS3**: Advanced styling with 3D effects
- **JavaScript ES6+**: Modern client-side functionality
- **WebSockets**: Real-time messaging protocol

## 🎯 Advanced Features

### Real-time Messaging
- **Instant Delivery**: Messages appear immediately
- **Connection Status**: Real-time connection monitoring
- **Auto-reconnection**: Automatic reconnection on connection loss
- **Message Queuing**: Reliable message delivery

### Message Management System
- **Individual Message Selection**: Click select button on any message
- **Bulk Selection**: Select multiple messages for batch operations
- **Per-Message Delete**: Delete individual messages with confirmation
- **Bulk Delete**: Delete multiple selected messages at once
- **Real-time Synchronization**: All users see deletions instantly
- **Message IDs**: Each message has a unique identifier for tracking

### Visual Enhancements
- **Loading Animations**: Smooth loading screens
- **Ripple Effects**: Interactive button feedback
- **Parallax Effects**: Subtle mouse-following animations
- **Smooth Transitions**: CSS transitions throughout
- **Hover Actions**: Message action buttons appear on hover
- **Selection Highlights**: Visual feedback for selected messages

### User Experience
- **Keyboard Shortcuts**: Enter to send, Shift+Enter for new line
- **Auto-resize**: Input area adapts to content
- **Clear Chat**: Option to clear conversation history
- **Visual Feedback**: Confirmation for all actions
- **Optimized Stickers**: Perfect size for chat (120px max)
- **Blue Theme**: Consistent blue color scheme throughout

## 🔄 Auto-Reply System

The app includes an intelligent auto-reply system:
- **Context-Aware**: Different replies for text vs stickers
- **Realistic Timing**: 8-second delay for natural conversation flow
- **Varied Responses**: Multiple reply options for variety
- **Emoji Integration**: Replies include relevant emojis

## 📱 Responsive Design

The interface adapts beautifully to different screen sizes:
- **Desktop**: Full sidebar and chat area
- **Tablet**: Optimized layout with touch-friendly elements
- **Mobile**: Collapsible sidebar with mobile-first design

## 🎨 Customization

Easy to customize:
- **Colors**: Modify CSS variables in style.css
- **Stickers**: Add more stickers to the static/stickers folder
- **Contacts**: Update the contacts list in app.py
- **Responses**: Modify auto-reply messages in app.py

## 🔧 Development

### File Structure
```
CipherChat/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── messages.json         # Message storage (auto-created)
├── templates/
│   └── index.html        # Main template
└── static/
    ├── css/
    │   └── style.css     # 3D styling
    ├── js/
    │   └── app.js        # Client-side logic
    ├── stickers/         # Sticker images
    │   ├── 1.png
    │   ├── 2.png
    │   └── ... (20 total)
    └── logo.png          # Your logo
```

### API Endpoints
- `GET /` - Main chat interface
- `GET /api/messages/<contact>` - Get messages for contact
- `POST /api/send_message` - Send new message
- `GET /api/stickers` - Get available stickers
- `DELETE /api/clear_chat/<contact>` - Clear chat with contact
- `POST /api/delete_messages` - Delete specific messages by ID

### WebSocket Events
- `connect` - Client connection
- `disconnect` - Client disconnection
- `join_chat` - Join chat room
- `leave_chat` - Leave chat room
- `new_message` - New message broadcast
- `user_typing` - Typing indicator
- `messages_deleted` - Broadcast message deletions
- `chat_cleared` - Broadcast chat clearing

## 🎮 How to Use Message Management

### Selecting Messages
1. **Hover over any message** to see action buttons
2. **Click the select button** (checkmark icon) to select a message
3. **Selected messages** will be highlighted with blue outline
4. **Bulk actions bar** appears at the bottom when messages are selected

### Deleting Messages
1. **Single Delete**: Click the delete button (trash icon) on any message
2. **Bulk Delete**: Select multiple messages and click "Delete Selected"
3. **Confirmation**: Messages are deleted immediately with visual feedback
4. **Real-time Updates**: All users see the deletions instantly

### Bulk Operations
1. **Select Multiple**: Click select button on multiple messages
2. **Bulk Actions Bar**: Appears at bottom showing selected count
3. **Deselect All**: Click to clear all selections
4. **Delete Selected**: Remove all selected messages at once

## 🚀 Performance

- **Optimized Loading**: Efficient resource loading
- **Smooth Animations**: Hardware-accelerated CSS animations
- **Minimal Bandwidth**: Efficient WebSocket communication
- **Caching**: Static assets cached for performance

## 🛡️ Security

- **Input Sanitization**: All user input properly escaped
- **CORS Protection**: Configured for secure cross-origin requests
- **Session Management**: Secure session handling
- **XSS Prevention**: Protected against cross-site scripting

## 🎉 Getting Started

1. **Clone/Download** the project
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run the server**: `python app.py`
4. **Open browser**: Go to `http://localhost:5000`
5. **Start chatting**: Click a contact and send your first message!
6. **Try message management**: Hover over messages to see action buttons
7. **Select and delete**: Practice selecting and deleting messages
8. **Send stickers**: Click the sticker button and send fun stickers!

## 🔥 New Features Summary

### ✅ What's New
- **Message Selection**: Click to select individual messages
- **Bulk Delete**: Select multiple messages and delete them together
- **Per-Message Actions**: Hover buttons for select and delete
- **Real-time Updates**: All users see deletions instantly
- **Optimized Stickers**: Perfect size for chat (120px max)
- **Blue Theme**: Consistent blue color scheme throughout
- **Enhanced Navbar**: White background with larger logo
- **Improved UX**: Better visual feedback and animations

### 🎯 Perfect For
- **Personal Use**: Organize your conversations
- **Team Chat**: Manage group conversations
- **Portfolio Projects**: Showcase modern web development skills
- **Learning**: Study real-time web application development
- **Customization**: Easy to modify and extend

Enjoy your modern, feature-rich web messaging experience with CipherChat! 🚀✨💙
