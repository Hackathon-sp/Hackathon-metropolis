import os
import imaplib
import json
import google.auth
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define OAuth2 Scopes for Gmail IMAP access
SCOPES = ["https://mail.google.com/"]

def get_oauth2_token():
    """Authenticate with Gmail API and generate an OAuth2 access token."""
    creds = None
    token_file = "token.json"
    credentials_file = "client_secret.json"

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return creds

if __name__ == "__main__":
    creds = get_oauth2_token()
    print("OAuth2 Token generated successfully!")
