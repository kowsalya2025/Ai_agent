document.addEventListener('DOMContentLoaded', () => {
    const chatToggle = document.getElementById('chatToggle');
    const chatContainer = document.getElementById('chatContainer');
    const closeChat = document.getElementById('closeChat');
    const chatBadge = document.querySelector('.chat-badge');
    
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendMessage');

    // Toggle logic
    chatToggle.addEventListener('click', () => {
        chatContainer.classList.remove('hidden');
        chatBadge.style.display = 'none';
        userInput.focus();
    });

    closeChat.addEventListener('click', () => {
        chatContainer.classList.add('hidden');
    });

    // Send Message
    const sendMessage = async () => {
        const text = userInput.value.trim();
        if (!text) return;

        // Append user message
        appendMessage(text, 'user');
        userInput.value = '';

        // Show typing indicator
        const typingId = showTypingIndicator();

        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            removeElement(typingId);

            if (data.reply) {
                appendMessage(data.reply, 'ai');
            } else {
                appendMessage("Error: Failed to connect to server.", 'ai');
            }

        } catch (err) {
            removeElement(typingId);
            appendMessage("Connection issue. Unable to reach Vanakam Guide AI at this time.", 'ai');
            console.error(err);
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function appendMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        msgDiv.appendChild(contentDiv);
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message ai';
        msgDiv.id = id;

        msgDiv.innerHTML = `
            <div class="message-content typing-indicator">
                <div class="typing-line"></div>
                <div class="typing-line"></div>
                <div class="typing-line"></div>
            </div>
        `;

        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }
});
