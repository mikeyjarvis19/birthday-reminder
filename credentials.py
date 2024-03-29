import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging_setup


logger = logging_setup.get_logger("credentials")


class CredsManager:
    """Setup creds"""

    def __init__(self):
        self.creds = self.setup_creds()

    def setup_creds(self):
        scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("credentials/token.pickle"):
            with open("credentials/token.pickle", "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials/credentials.json", scopes
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("credentials/token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return creds
