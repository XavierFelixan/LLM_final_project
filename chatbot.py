import random

RESPONSES = {
    'greeting': 'Hello! I am your local chatbot. What can I help you with today?',
    'status': 'I am doing great, thanks! I was built to chat and answer simple questions.',
    'name': 'I am a simple chatbot interface demo built for a website. You can call me "Chatbot".',
    'weather': 'I can talk about many things, but I do not have real-time weather data yet.',
    'help': 'Try asking me a question, introducing yourself, or saying hello. I can echo your message and reply with simple responses.',
}

def generate_response(message: str) -> str:
    text = message.strip().lower()
    if not text:
        return 'Please type something so I can respond.'

    if any(word in text for word in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']):
        return RESPONSES['greeting']

    if 'how are you' in text or 'how are u' in text:
        return RESPONSES['status']

    if 'name' in text:
        return RESPONSES['name']

    if 'weather' in text:
        return RESPONSES['weather']

    if 'help' in text or 'what can you do' in text:
        return RESPONSES['help']

    if text.endswith('?'):
        return 'That is an interesting question. I am still learning how to answer smarter questions!'

    return f'You said: "{message}". I am a chatbot prototype, so I can repeat your message and give a sample answer.'

if __name__ == '__main__':
    print('Local chatbot test. Type "exit" or press Ctrl+C to quit.')
    try:
        while True:
            user = input('> ').strip()
            if user.lower() in ('exit', 'quit'):
                break
            print(generate_response(user))
    except KeyboardInterrupt:
        print('\nGoodbye!')
