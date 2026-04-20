import datetime
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytz

# Scope: full access to calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

class Calendar:
    def __init__(self):
        creds = None
        # Load saved token if available
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If no valid credentials, log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)


    def get_event_ids(self, **kwargs):
        max_results = kwargs.get('max_results', 5)
        query = kwargs.get('query')
        tz = pytz.timezone("Asia/Hong_Kong")
        now = kwargs.get('now', datetime.datetime.now(tz).isoformat())
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime',
            q=query  
        ).execute()
        events = events_result.get('items', [])
        results = []
        for event in events:
            results.append({
                'id': event['id'],
                'summary': event.get('summary'),
                'start': event['start'].get('dateTime', event['start'].get('date'))
            })
        return str([event['id'] for event in events]) if events else "No such events found."


    def set_new_event(self, **kwargs):
        # Example: create an event
        print("Creating event with arguments")
        event = {
            'summary': kwargs.get('summary'),
            'location': kwargs.get('location', None),
            'description': kwargs.get('description', None),
            'start': kwargs.get('start'),
            'end': kwargs.get('end')
        }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

        return "Event created successfully."


    def list_upcoming_events(self, **kwargs):
        max_results = kwargs.get('max_results', 10)
        tz = pytz.timezone("Asia/Hong_Kong")
        now = datetime.datetime.now(tz).isoformat()
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            results = "No upcoming events found."
        else:
            results = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                print(start, event['summary'])
                results.append((start, end, event['summary'], event['id']))

        return str(results)


    def delete_event(self, **kwargs):
        # event_ids = self.get_event_ids(kwargs['query'])
        event_id = kwargs['event_id']
        log = ""
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            print(f'Event {event_id} deleted successfully.')
            log += f'Event {event_id} deleted successfully.\n'

        except Exception as e:
            print(f'An error occurred: {e}')
            return f'Failed to delete event: {e}'

        return log


    def update_event(self, **kwargs):
        event_id = kwargs['event_id']
        log = ""
        try:
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
            for key, value in kwargs.items():
                event[key] = value

            updated_event = self.service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()
            print('Event updated: %s' % updated_event.get('htmlLink'))
            log += f'Event {event_id} updated successfully.\n'
        except Exception as e:
            print(f'An error occurred: {e}')
            return f'Failed to update event: {e}'

        return log