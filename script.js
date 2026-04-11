const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

function appendMessage(role, text) {
  const bubble = document.createElement('div');
  bubble.className = `chat-message ${role}`;
  bubble.textContent = text;
  chatWindow.appendChild(bubble);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function getBotReply(message) {
  if (!message.trim()) {
    return 'Please type something so I can respond.';
  }

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error('Server error');
    }

    const data = await response.json();
    return data.response || 'Sorry, something went wrong.';
  } catch (error) {
    return 'Unable to reach the chatbot server. Please check that the Flask app is running.';
  }
}

chatForm.addEventListener('submit', async event => {
  event.preventDefault();
  const value = userInput.value.trim();
  if (!value) return;

  appendMessage('user', value);
  userInput.value = '';
  userInput.focus();

  appendMessage('bot', 'Typing...');
  const reply = await getBotReply(value);

  const lastBot = document.querySelector('.chat-message.bot:last-child');
  if (lastBot) {
    lastBot.remove();
  }

  appendMessage('bot', reply);
});
