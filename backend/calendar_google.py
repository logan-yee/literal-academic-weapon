from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials.json (from Google Cloud Console)
SCOPES = ["https://www.googleapis.com/auth/calendar"]
creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

# Build the Calendar API service
service = build("calendar", "v3", credentials=creds)
