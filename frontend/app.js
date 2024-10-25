// frontend/app.js

// Base URL of your Flask API
const API_BASE_URL = 'http://127.0.0.1:5000';

// Variables to keep track of the current conversation
let currentConversationId = null;

// Event listeners
document.getElementById('start-conversation-btn').addEventListener('click', startConversation);
document.getElementById('send-message-btn').addEventListener('click', sendMessage);
document.getElementById('retrieve-history-btn').addEventListener('click', retrieveHistory);
document.getElementById('clear-history-btn').addEventListener('click', clearHistory);
document.getElementById('delete-conversation-btn').addEventListener('click', deleteConversation);

// Function to start a new conversation
function startConversation() {
    fetch(`${API_BASE_URL}/conversations`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        currentConversationId = data.conversation_id;
        document.getElementById('conversation-id-display').innerText = `Conversation ID: ${currentConversationId}`;
        document.getElementById('conversation-id-input').value = currentConversationId;
        alert('New conversation started!');
        // Clear the chat window
        document.getElementById('chat-window').innerHTML = '';
    })
    .catch(error => {
        console.error('Error starting conversation:', error);
    });
}

// Function to send a message
function sendMessage() {
    const conversationId = document.getElementById('conversation-id-input').value;
    const messageContent = document.getElementById('message-input').value;

    if (!conversationId) {
        alert('Please enter a conversation ID.');
        return;
    }
    if (!messageContent) {
        alert('Please enter a message.');
        return;
    }

    fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: messageContent })
    })
    .then(response => response.json())
    .then(data => {
        // Update the chat window with the user's message and assistant's reply
        appendMessage('user', messageContent);
        appendMessage('assistant', data.assistant_reply);
        // Clear the message input
        document.getElementById('message-input').value = '';
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
}

// Function to retrieve chat history
function retrieveHistory() {
    const conversationId = document.getElementById('history-conversation-id-input').value;
    let url = '';

    if (conversationId) {
        url = `${API_BASE_URL}/conversations/${conversationId}/messages`;
    } else {
        url = `${API_BASE_URL}/conversations/messages`;
    }

    fetch(url)
    .then(response => response.json())
    .then(messages => {
        const historyDisplay = document.getElementById('history-display');
        historyDisplay.innerHTML = '';
        messages.forEach(msg => {
            const messageElement = document.createElement('p');
            messageElement.innerText = `[${msg.timestamp}] | ${msg.conversation_id} | (${msg.role}): ${msg.content}`;
            historyDisplay.appendChild(messageElement);
        });
    })
    .catch(error => {
        console.error('Error retrieving history:', error);
    });
}

// Function to clear conversation history
function clearHistory() {
    const conversationId = document.getElementById('clear-conversation-id-input').value;

    if (!conversationId) {
        alert('Please enter a conversation ID.');
        return;
    }

    fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // Clear the chat window if the current conversation was cleared
        if (conversationId == currentConversationId) {
            document.getElementById('chat-window').innerHTML = '';
        }
    })
    .catch(error => {
        console.error('Error clearing history:', error);
    });
}

// Function to delete a conversation
function deleteConversation() {
    const conversationId = document.getElementById('delete-conversation-id-input').value;

    if (!conversationId) {
        alert('Please enter a conversation ID.');
        return;
    }

    fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // Clear the chat window if the current conversation was deleted
        if (conversationId == currentConversationId) {
            document.getElementById('chat-window').innerHTML = '';
            document.getElementById('conversation-id-display').innerText = '';
            document.getElementById('conversation-id-input').value = '';
            currentConversationId = null;
        }
    })
    .catch(error => {
        console.error('Error deleting conversation:', error);
    });
}

// Helper function to append a message to the chat window
function appendMessage(role, content) {
    const chatWindow = document.getElementById('chat-window');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', role);
    messageElement.innerText = `${role === 'user' ? 'You' : 'Assistant'}: ${content}`;
    chatWindow.appendChild(messageElement);
    // Scroll to the bottom of the chat window
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
