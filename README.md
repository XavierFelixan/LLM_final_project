# Agentda Schedule Manager

Agentda is an AI Chatbot schedule manager that integrates seamlessly with your Google Calendar.

## Files

- `/static/index.html` — main website page
- `/static/styles.css` — interface styling
- `/static/script.js` — chat interaction logic
- `backend.py` — local file server launcher
- `ai.py` — AI agent
- `calendar_manager.py` — calendar manager object to connect with Google Calendar

## Run locally

1. Install all requirements if needed:

```bash
pip install -r requirements.txt
```

2. Run the Flask app:

```bash
python backend.py
```

3. Your browser should open automatically. If it does not, go to:

```text
http://127.0.0.1:8000/
```

## Notes

The chatbot page is served by Flask and the bot replies are generated through a simple backend API at `/api/chat`.
In order to see changes in Google Calendar for the end-to-end workflow, feel free to use a built dummy email. All credentials are in `.env` file. The current state of the project is built in accordance to that dummy email.
