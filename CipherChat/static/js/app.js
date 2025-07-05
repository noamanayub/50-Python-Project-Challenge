// CipherChat - Modern Messaging App JavaScript
class CipherChat {
    constructor() {
        this.socket = null;
        this.currentContact = null;
        this.messages = {};
        this.stickers = [];
        this.isTyping = false;
        this.typingTimeout = null;
        this.selectedMessages = new Set();
        
        this.init();
    }

    init() {
        this.showLoading();
        this.setupSocketIO();
        this.setupEventListeners();
        this.updateTime();
        this.loadStickers();
        
        // Hide loading after initialization
        setTimeout(() => {
            this.hideLoading();
        }, 2000);
    }

    showLoading() {
        const loading = document.getElementById('loadingOverlay');
        loading.style.display = 'flex';
    }

    hideLoading() {
        const loading = document.getElementById('loadingOverlay');
        loading.style.opacity = '0';
        setTimeout(() => {
            loading.style.display = 'none';
        }, 500);
    }

    setupSocketIO() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Connected to CipherChat server');
            this.showToast('Connected to CipherChat!', 'success');
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.showToast('Connection lost. Reconnecting...', 'warning');
        });

        this.socket.on('new_message', (data) => {
            if (data.contact === this.currentContact) {
                this.displayMessage(data.message, data.message.sender === 'You' ? 'sent' : 'received');
                this.scrollToBottom();
            }
            this.updateContactIndicator(data.contact);
        });

        this.socket.on('user_typing', (data) => {
            if (data.contact === this.currentContact && data.user !== 'You') {
                this.showTypingIndicator(data.user);
            }
        });

        this.socket.on('messages_deleted', (data) => {
            if (data.contact === this.currentContact) {
                // Remove deleted messages from UI
                data.message_ids.forEach(messageId => {
                    const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
                    if (messageElement) {
                        messageElement.remove();
                    }
                });
                
                // Clear selection
                this.clearSelection();
                
                this.showToast(`${data.deleted_count} message(s) deleted`, 'success');
            }
        });

        this.socket.on('chat_cleared', (data) => {
            if (data.contact === this.currentContact) {
                this.loadMessages(this.currentContact);
                this.showToast(`Chat with ${data.contact} cleared`, 'success');
            }
        });
    }

    setupEventListeners() {
        // Contact selection
        document.getElementById('contactsList').addEventListener('click', (e) => {
            const contactItem = e.target.closest('.contact-item');
            if (contactItem) {
                const contact = contactItem.dataset.contact;
                this.selectContact(contact);
            }
        });

        // Message input
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');

        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        messageInput.addEventListener('input', () => {
            this.handleTyping();
            this.updateSendButton();
        });

        sendBtn.addEventListener('click', () => {
            this.sendMessage();
        });

        // Sticker modal
        document.getElementById('stickerBtn').addEventListener('click', () => {
            this.showStickerModal();
        });

        document.getElementById('closeStickerModal').addEventListener('click', () => {
            this.hideStickerModal();
        });

        // Clear chat
        document.getElementById('clearChatBtn').addEventListener('click', () => {
            this.clearCurrentChat();
        });

        // Modal close on outside click
        document.getElementById('stickerModal').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) {
                this.hideStickerModal();
            }
        });

        // Auto-resize textarea
        messageInput.addEventListener('input', () => {
            this.autoResizeTextarea(messageInput);
        });

        // Bulk actions
        document.getElementById('deselectAllBtn').addEventListener('click', () => {
            this.clearSelection();
        });

        document.getElementById('deleteSelectedBtn').addEventListener('click', () => {
            this.deleteSelectedMessages();
        });

        // Message selection (event delegation)
        document.getElementById('messagesContainer').addEventListener('click', (e) => {
            const messageElement = e.target.closest('.message-bubble');
            if (messageElement) {
                const messageId = messageElement.dataset.messageId;
                if (e.target.classList.contains('select-message-btn')) {
                    // Toggle selection when clicking the select button
                    this.toggleMessageSelection(messageId);
                } else if (e.target.classList.contains('delete-message-btn')) {
                    // Delete single message when clicking the delete button
                    this.deleteSingleMessage(messageId);
                }
            }
        });
    }

    selectContact(contact) {
        // Update UI
        const contactItems = document.querySelectorAll('.contact-item');
        contactItems.forEach(item => {
            item.classList.remove('active');
            if (item.dataset.contact === contact) {
                item.classList.add('active');
            }
        });

        // Update chat header
        document.getElementById('chatUserName').textContent = contact;
        document.getElementById('chatUserStatus').textContent = 'Online';

        // Leave previous room and join new room
        if (this.currentContact) {
            this.socket.emit('leave_chat', { contact: this.currentContact });
        }
        
        this.currentContact = contact;
        this.socket.emit('join_chat', { contact: contact });

        // Load messages for this contact
        this.loadMessages(contact);
    }

    async loadMessages(contact) {
        try {
            const response = await fetch(`/api/messages/${contact}`);
            const messages = await response.json();
            
            this.messages[contact] = messages;
            this.displayMessages(messages);
        } catch (error) {
            console.error('Error loading messages:', error);
            this.showToast('Error loading messages', 'error');
        }
    }

    displayMessages(messages) {
        const container = document.getElementById('messagesContainer');
        container.innerHTML = '';

        if (messages.length === 0) {
            container.innerHTML = `
                <div class="welcome-message">
                    <div class="welcome-content">
                        <i class="fas fa-comments"></i>
                        <h3>Start Chatting!</h3>
                        <p>Send a message to ${this.currentContact}</p>
                    </div>
                </div>
            `;
            return;
        }

        messages.forEach(message => {
            this.displayMessage(message, message.sender === 'You' ? 'sent' : 'received', false);
        });

        this.scrollToBottom();
    }

    displayMessage(message, type, animate = true) {
        const container = document.getElementById('messagesContainer');
        
        // Remove welcome message if exists
        const welcomeMessage = container.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message-bubble ${type}`;
        messageDiv.dataset.messageId = message.id; // Add data attribute for message ID
        
        if (animate) {
            messageDiv.style.opacity = '0';
            messageDiv.style.transform = 'translateY(20px)';
        }

        let content = '';
        if (message.type === 'sticker') {
            content = `
                <div class="message-content">
                    <img src="/static/stickers/${message.message}" alt="Sticker" class="message-sticker">
                    <div class="message-time">${message.timestamp}</div>
                </div>
                <div class="message-actions">
                    <button class="message-action-btn select-message-btn" title="Select message">
                        <i class="fas fa-check"></i>
                    </button>
                    <button class="message-action-btn delete-message-btn" title="Delete message">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
        } else {
            content = `
                <div class="message-content">
                    <div class="message-text">${this.escapeHtml(message.message)}</div>
                    <div class="message-time">${message.timestamp}</div>
                </div>
                <div class="message-actions">
                    <button class="message-action-btn select-message-btn" title="Select message">
                        <i class="fas fa-check"></i>
                    </button>
                    <button class="message-action-btn delete-message-btn" title="Delete message">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
        }

        messageDiv.innerHTML = content;
        container.appendChild(messageDiv);

        if (animate) {
            setTimeout(() => {
                messageDiv.style.transition = 'all 0.3s ease-out';
                messageDiv.style.opacity = '1';
                messageDiv.style.transform = 'translateY(0)';
            }, 50);
        }

        this.scrollToBottom();
    }

    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();

        if (!message || !this.currentContact) return;

        try {
            const response = await fetch('/api/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contact: this.currentContact,
                    message: message,
                    sender: 'You',
                    type: 'text'
                })
            });

            if (response.ok) {
                messageInput.value = '';
                this.updateSendButton();
                this.autoResizeTextarea(messageInput);
                
                // Show visual feedback
                this.showSendFeedback();
            } else {
                throw new Error('Failed to send message');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.showToast('Failed to send message', 'error');
        }
    }

    async sendSticker(stickerId) {
        if (!this.currentContact) return;

        try {
            const response = await fetch('/api/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contact: this.currentContact,
                    message: `${stickerId}.png`,
                    sender: 'You',
                    type: 'sticker'
                })
            });

            if (response.ok) {
                this.hideStickerModal();
                this.showToast('Sticker sent!', 'success');
            } else {
                throw new Error('Failed to send sticker');
            }
        } catch (error) {
            console.error('Error sending sticker:', error);
            this.showToast('Failed to send sticker', 'error');
        }
    }

    async loadStickers() {
        try {
            const response = await fetch('/api/stickers');
            this.stickers = await response.json();
            this.renderStickers();
        } catch (error) {
            console.error('Error loading stickers:', error);
            this.showToast('Error loading stickers', 'error');
        }
    }

    renderStickers() {
        const stickerGrid = document.getElementById('stickerGrid');
        stickerGrid.innerHTML = '';

        this.stickers.forEach(sticker => {
            const stickerElement = document.createElement('img');
            stickerElement.src = `/static/${sticker.url}`;
            stickerElement.alt = `Sticker ${sticker.id}`;
            stickerElement.className = 'sticker-item';
            stickerElement.addEventListener('click', () => {
                this.sendSticker(sticker.id);
            });
            stickerGrid.appendChild(stickerElement);
        });
    }

    showStickerModal() {
        document.getElementById('stickerModal').style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    hideStickerModal() {
        document.getElementById('stickerModal').style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    clearCurrentChat() {
        if (!this.currentContact) {
            this.showToast('Please select a contact first', 'warning');
            return;
        }

        if (confirm(`Clear all messages with ${this.currentContact}?`)) {
            this.deleteChatFromServer(this.currentContact);
        }
    }

    async deleteChatFromServer(contact) {
        try {
            // Show loading state
            const clearBtn = document.getElementById('clearChatBtn');
            const originalIcon = clearBtn.innerHTML;
            clearBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            clearBtn.disabled = true;

            const response = await fetch(`/api/clear_chat/${contact}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                const result = await response.json();
                // Clear messages from local memory
                this.messages[contact] = [];
                
                // Update UI immediately
                this.displayMessages([]);
                
                this.showToast(result.message, 'success');
            } else {
                throw new Error('Failed to clear chat');
            }
        } catch (error) {
            console.error('Error clearing chat:', error);
            this.showToast('Failed to clear chat', 'error');
        } finally {
            // Restore button state
            const clearBtn = document.getElementById('clearChatBtn');
            clearBtn.innerHTML = '<i class="fas fa-trash"></i>';
            clearBtn.disabled = false;
        }
    }

    // Message Selection Methods
    toggleMessageSelection(messageId) {
        const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
        if (!messageElement) return;

        if (this.selectedMessages.has(messageId)) {
            this.selectedMessages.delete(messageId);
            messageElement.classList.remove('selected');
        } else {
            this.selectedMessages.add(messageId);
            messageElement.classList.add('selected');
        }

        this.updateBulkActionsBar();
    }

    clearSelection() {
        this.selectedMessages.clear();
        document.querySelectorAll('.message-bubble.selected').forEach(element => {
            element.classList.remove('selected');
        });
        this.updateBulkActionsBar();
    }

    updateBulkActionsBar() {
        const bulkActions = document.getElementById('bulkActions');
        const bulkActionsText = document.getElementById('bulkActionsText');
        const selectedCount = this.selectedMessages.size;

        if (selectedCount > 0) {
            bulkActions.classList.add('show');
            bulkActionsText.textContent = `${selectedCount} message${selectedCount > 1 ? 's' : ''} selected`;
        } else {
            bulkActions.classList.remove('show');
        }
    }

    async deleteSelectedMessages() {
        if (this.selectedMessages.size === 0) {
            this.showToast('No messages selected', 'warning');
            return;
        }

        const messageIds = Array.from(this.selectedMessages);
        const confirmMessage = `Delete ${messageIds.length} selected message${messageIds.length > 1 ? 's' : ''}?`;
        
        if (!confirm(confirmMessage)) {
            return;
        }

        try {
            const response = await fetch('/api/delete_messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contact: this.currentContact,
                    message_ids: messageIds
                })
            });

            if (response.ok) {
                // The socket event will handle UI updates
                this.showToast('Messages deleted successfully', 'success');
            } else {
                throw new Error('Failed to delete messages');
            }
        } catch (error) {
            console.error('Error deleting messages:', error);
            this.showToast('Error deleting messages', 'error');
        }
    }

    async deleteSingleMessage(messageId) {
        if (!confirm('Delete this message?')) {
            return;
        }

        try {
            const response = await fetch('/api/delete_messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contact: this.currentContact,
                    message_ids: [messageId]
                })
            });

            if (response.ok) {
                this.showToast('Message deleted successfully', 'success');
            } else {
                throw new Error('Failed to delete message');
            }
        } catch (error) {
            console.error('Error deleting message:', error);
            this.showToast('Error deleting message', 'error');
        }
    }

    handleTyping() {
        if (!this.currentContact) return;

        if (!this.isTyping) {
            this.isTyping = true;
            this.socket.emit('user_typing', {
                contact: this.currentContact,
                user: 'You',
                typing: true
            });
        }

        clearTimeout(this.typingTimeout);
        this.typingTimeout = setTimeout(() => {
            this.isTyping = false;
            this.socket.emit('user_typing', {
                contact: this.currentContact,
                user: 'You',
                typing: false
            });
        }, 1000);
    }

    showTypingIndicator(user) {
        const container = document.getElementById('messagesContainer');
        let indicator = container.querySelector('.typing-indicator');
        
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = 'typing-indicator';
            indicator.innerHTML = `
                <span>${user} is typing</span>
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            `;
            container.appendChild(indicator);
        }

        // Remove after 3 seconds
        setTimeout(() => {
            if (indicator && indicator.parentNode) {
                indicator.remove();
            }
        }, 3000);

        this.scrollToBottom();
    }

    updateSendButton() {
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        
        if (messageInput.value.trim() && this.currentContact) {
            sendBtn.disabled = false;
            sendBtn.style.opacity = '1';
        } else {
            sendBtn.disabled = true;
            sendBtn.style.opacity = '0.5';
        }
    }

    showSendFeedback() {
        const sendBtn = document.getElementById('sendBtn');
        const originalHTML = sendBtn.innerHTML;
        
        sendBtn.innerHTML = '<i class="fas fa-check"></i>';
        sendBtn.style.background = 'linear-gradient(135deg, #28a745, #20c997)';
        
        setTimeout(() => {
            sendBtn.innerHTML = originalHTML;
            sendBtn.style.background = 'linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%)';
        }, 1000);
    }

    updateContactIndicator(contact) {
        const contactItem = document.querySelector(`[data-contact="${contact}"]`);
        if (contactItem) {
            const indicator = contactItem.querySelector('.contact-indicator');
            indicator.style.animation = 'pulse 0.5s';
            setTimeout(() => {
                indicator.style.animation = '';
            }, 500);
        }
    }

    autoResizeTextarea(textarea) {
        textarea.style.height = '45px';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    scrollToBottom() {
        const container = document.getElementById('messagesContainer');
        setTimeout(() => {
            container.scrollTop = container.scrollHeight;
        }, 100);
    }

    updateTime() {
        const updateClock = () => {
            const now = new Date();
            const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            document.getElementById('currentTime').textContent = time;
        };

        updateClock();
        setInterval(updateClock, 1000);
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('notificationToast');
        const toastMessage = document.getElementById('toastMessage');
        
        toastMessage.textContent = message;
        
        // Update colors based on type
        if (type === 'success') {
            toast.style.background = 'linear-gradient(135deg, #28a745, #20c997)';
        } else if (type === 'error') {
            toast.style.background = 'linear-gradient(135deg, #dc3545, #e74c3c)';
        } else if (type === 'warning') {
            toast.style.background = 'linear-gradient(135deg, #ffc107, #ffb300)';
        } else {
            toast.style.background = 'linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%)';
        }
        
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CipherChat();
});

// Add some visual effects
document.addEventListener('DOMContentLoaded', () => {
    // Add parallax effect to background
    document.addEventListener('mousemove', (e) => {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            navbar.style.transform = `translateX(${mouseX * 10}px) translateY(${mouseY * 5}px)`;
        }
    });

    // Add click ripple effect
    const addRippleEffect = (element) => {
        element.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    };

    // Add ripple effect to buttons
    document.querySelectorAll('.send-btn, .input-btn, .action-btn').forEach(addRippleEffect);
});

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.4);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
