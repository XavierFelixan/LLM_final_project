# Agentda - Your Agent-based Schedule Manager

Agentda is an AI Chatbot schedule manager that integrates seamlessly with your Google Calendar.

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

## Google Calendar API Setup
If you cannot use the given credentials.json or token.json, or if you want this application appleid your own Google Calendar, please follow these steps to set up your own Google Calendar API.

### Step 1: Enable Google Calendar API
1. Go to [Google Cloud Console](https://console.cloud.google.com).
2. Create/select a project.
3. Enable **Google Calendar API** under *APIs & Services → Library*.

### Step 2: Configure OAuth Consent Screen
1. Navigate to *APIs & Services → OAuth consent screen*.
2. Set up application type (External for testing).
3. Fill in required fields and save.
4. Scroll down to the **Test users** section.  
5. Click **Add users** and enter the Gmail addresses of each person who will use the agent.  

### Step 3: Create OAuth Credentials
1. Go to *APIs & Services → Credentials*.
2. Click **Create Credentials → OAuth client ID**.
3. Choose **Desktop application**.
4. Download the `credentials.json` file.

### Step 4: Place Credentials in Repo
1. Save `credentials.json` in the project root.

### Step 5: Authenticate
1. Run the agent once. A browser window will open for Google login.  
2. Follow instructions to generate a `token.json` file that stores the user’s access/refresh tokens.

### Step 6: Verify
1. Run a test command (e.g., list upcoming events).
2. Confirm that events are correctly retrieved/created in the user’s calendar.