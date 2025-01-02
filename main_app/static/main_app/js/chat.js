document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.querySelector('.messages');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendBtn');

    sendButton.addEventListener('click', () => {
        const message = messageInput.value.trim();
        if (message) {
            const newMessage = document.createElement('div');
            newMessage.className = 'message sent';
            newMessage.innerHTML = `<p>${message}</p>`;
            messagesContainer.appendChild(newMessage);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            messageInput.value = '';
        }
    });
});
