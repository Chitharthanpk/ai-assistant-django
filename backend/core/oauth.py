import os
import pathlib
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load environment or static secret file path
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'client_secret.json')  # <-- Update if path is different

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly',
]

# Redirect URI from .env or fallback
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", 'http://127.0.0.1:8000/api/oauth/google/callback/')

# Google Client details
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


def get_flow(state=None):
    """Returns a configured OAuth 2.0 flow object"""
    return Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state=state 
    )

def get_credentials_from_code(code):
    """Exchange auth code for credentials"""
    flow = get_flow()
    flow.fetch_token(code=code)
    return flow.credentials

def refresh_token(credentials_dict):
    """Refresh expired credentials using refresh_token"""
    credentials = Credentials(
        token=None,
        refresh_token=credentials_dict['refresh_token'],
        token_uri='https://oauth2.googleapis.com/token',
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=SCOPES,
    )
    credentials.refresh(Request())
    return credentials


import requests

def get_user_info(credentials):
    """Fetch user profile info from Google using access token."""
    response = requests.get(
        'https://www.googleapis.com/oauth2/v1/userinfo',
        params={'alt': 'json'},
        headers={'Authorization': f'Bearer {credentials.token}'}
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch user info: {response.text}")