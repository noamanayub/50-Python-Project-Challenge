from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cipherChat2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables
messages = {}
users = {}
contacts = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

def load_messages():
    """Load messages from JSON file"""
    global messages
    try:
        if os.path.exists('messages.json'):
            with open('messages.json', 'r') as f:
                messages = json.load(f)
    except:
        messages = {}

def save_messages():
    """Save messages to JSON file"""
    try:
        with open('messages.json', 'w') as f:
            json.dump(messages, f, indent=2)
    except Exception as e:
        print(f"Error saving messages: {e}")

@app.route('/')
def home():
    """Home page with chat interface"""
    return render_template('index.html', contacts=contacts)

@app.route('/api/messages/<contact>')
def get_messages(contact):
    """Get messages for a specific contact"""
    if contact in messages:
        return jsonify(messages[contact])
    return jsonify([])

@app.route('/api/send_message', methods=['POST'])
def send_message():
    """Send a new message"""
    data = request.get_json()
    contact = data.get('contact')
    message = data.get('message')
    sender = data.get('sender', 'You')
    msg_type = data.get('type', 'text')
    
    if contact not in messages:
        messages[contact] = []
    
    new_message = {
        'id': str(uuid.uuid4()),
        'sender': sender,
        'message': message,
        'type': msg_type,
        'timestamp': datetime.now().strftime('%H:%M')
    }
    
    messages[contact].append(new_message)
    save_messages()
    
    # Emit to all connected clients
    socketio.emit('new_message', {
        'contact': contact,
        'message': new_message
    })
    
    return jsonify({'status': 'success', 'message': new_message})

@app.route('/api/stickers')
def get_stickers():
    """Get available stickers"""
    stickers = []
    sticker_dir = 'static/stickers'
    if os.path.exists(sticker_dir):
        for i in range(1, 21):
            sticker_path = f'stickers/{i}.png'
            if os.path.exists(f'static/{sticker_path}'):
                stickers.append({
                    'id': i,
                    'url': sticker_path
                })
    return jsonify(stickers)

@app.route('/api/clear_chat/<contact>', methods=['DELETE'])
def clear_chat(contact):
    """Clear all messages for a specific contact"""
    global messages
    if contact in messages:
        messages[contact] = []
        save_messages()
        
        # Emit to all connected clients
        socketio.emit('chat_cleared', {
            'contact': contact
        })
        
        return jsonify({'status': 'success', 'message': f'Chat with {contact} cleared'})
    return jsonify({'status': 'error', 'message': 'Contact not found'})

@app.route('/api/delete_messages', methods=['POST'])
def delete_messages():
    """Delete specific messages by their IDs"""
    data = request.get_json()
    contact = data.get('contact')
    message_ids = data.get('message_ids', [])
    
    if contact not in messages:
        return jsonify({'status': 'error', 'message': 'Contact not found'})
    
    # Filter out messages with the specified IDs
    original_count = len(messages[contact])
    messages[contact] = [msg for msg in messages[contact] if msg['id'] not in message_ids]
    deleted_count = original_count - len(messages[contact])
    
    save_messages()
    
    # Emit to all connected clients
    socketio.emit('messages_deleted', {
        'contact': contact,
        'message_ids': message_ids,
        'deleted_count': deleted_count
    })
    
    return jsonify({
        'status': 'success', 
        'message': f'{deleted_count} message(s) deleted',
        'deleted_count': deleted_count
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f'Client connected: {request.sid}')
    emit('connected', {'message': 'Connected to CipherChat'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f'Client disconnected: {request.sid}')

@socketio.on('join_chat')
def handle_join_chat(data):
    """Handle joining a chat room"""
    contact = data['contact']
    join_room(contact)
    emit('joined_chat', {'contact': contact})

@socketio.on('leave_chat')
def handle_leave_chat(data):
    """Handle leaving a chat room"""
    contact = data['contact']
    leave_room(contact)
    emit('left_chat', {'contact': contact})

def simulate_auto_reply():
    """Simulate auto-reply from contacts"""
    import threading
    import time
    import random
    
    def auto_reply_worker():
        while True:
            time.sleep(8)  # Wait 8 seconds
            
            # Check for recent messages to reply to
            for contact in contacts:
                if contact in messages and messages[contact]:
                    last_msg = messages[contact][-1]
                    if last_msg['sender'] == 'You':
                        # Generate auto-reply
                        if last_msg['type'] == 'sticker':
                            replies = [
                                "Haha! Great sticker! 😄",
                                "Love that one! 🎉",
                                "Nice choice! 👍",
                                "That's hilarious! 😂",
                                "Perfect! 💯"
                            ]
                        else:
                            replies = [
                                "That's really interesting! 🤔",
                                "I completely agree! 👍",
                                "Thanks for sharing that! 😊",
                                "Wow, that's cool! 🔥",
                                "Got it, thanks! ✅",
                                "Absolutely right! 💯",
                                "Great point! 🎯",
                                "I see what you mean! 👀"
                            ]
                        
                        reply = random.choice(replies)
                        
                        # Add auto-reply
                        auto_message = {
                            'id': str(uuid.uuid4()),
                            'sender': contact,
                            'message': reply,
                            'type': 'text',
                            'timestamp': datetime.now().strftime('%H:%M')
                        }
                        
                        messages[contact].append(auto_message)
                        save_messages()
                        
                        # Emit to all clients
                        socketio.emit('new_message', {
                            'contact': contact,
                            'message': auto_message
                        })
    
    thread = threading.Thread(target=auto_reply_worker, daemon=True)
    thread.start()

if __name__ == '__main__':
    # Load existing messages
    load_messages()
    
    # Start auto-reply simulation
    simulate_auto_reply()
    
    # Run the Flask app
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
