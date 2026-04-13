# Agentda - Your Agent-based Schedule Manager

This project contains an agent-based schedule manager system integrated with Google Calendar

## Files

- `/static/index.html` — main website page
- `/static/styles.css` — interface styling
- `/static/script.js` — chat interaction logic
- `backend.py` — local file server launcher
- `ai.py` — AI agent
- `calendar_manager.py` — calendar manager object to connect with Google Calendar
- `requirements.txt` — necessary libraries and frameworks to run this application
- `tools.json` — tools that the AI agent has access to

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
Within `.gitignore`, files such as `token.json` and `credentials.json` are critical to support the Google Calendar API. Please substitute with your own JSON files accordingly when setting up and enabling your own Google account's Google Calendar API. 