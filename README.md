# Simple Chatbot Website

This project contains a simple chatbot-like website interface with a local frontend.

## Files

- `index.html` — main website page
- `styles.css` — interface styling
- `script.js` — chat interaction logic
- `frontend.py` — local file server launcher
- `chatbot.py` — simple chatbot response helper

## Run locally

1. Install Flask if needed:

```bash
pip install flask
```

2. Run the Flask app:

```bash
python frontend.py
```

3. Your browser should open automatically. If it does not, go to:

```text
http://127.0.0.1:8000/
```

## Notes

The chatbot page is served by Flask and the bot replies are generated through a simple backend API at `/api/chat`.
