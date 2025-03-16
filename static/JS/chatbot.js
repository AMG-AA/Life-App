function toggleChatbot() {
    const chatbotWindow = document.getElementById('chatbot-window');
    const isVisible = chatbotWindow.style.display === 'flex';

    // Cambiar la visibilidad de la ventana del chatbot
    chatbotWindow.style.display = isVisible ? 'none' : 'flex'; // Usamos 'flex' para asegurar la visibilidad
}

// Función para cerrar el chatbot
function closeChatbot() {
    const chatbotWindow = document.getElementById('chatbot-window');
    // Ocultar la ventana del chatbot inmediatamente
    chatbotWindow.style.display = 'none';
}

async function sendChatbotMessage() {
    const question = document.getElementById('chatbot-question').value;
    const messageContainer = document.getElementById('chatbot-messages');

    if (!question.trim()) return;

    // Show first question in chatbot window
    const userMessage = document.createElement('div');
    userMessage.textContent = 'You: ' + question;
    userMessage.style.marginBottom = '10px';
    messageContainer.appendChild(userMessage);

    // Send question to chatbot API
    const response = await fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question })
    });
    const data = await response.json();

    // Show chatbot response in chatbot window
    const botMessage = document.createElement('div');
    botMessage.textContent = 'Chatbot: ' + data.answer;
    botMessage.style.marginBottom = '10px';
    botMessage.style.color = '#007bff';
    messageContainer.appendChild(botMessage);

    // Scroll to bottom of chatbot window
    messageContainer.scrollTop = messageContainer.scrollHeight

    // Clear input field
    document.getElementById('chatbot-question').value = '';
}