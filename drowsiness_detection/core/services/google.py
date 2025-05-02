import pickle
import os
from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from drowsiness_detection.apps.users.model import User


def googledrive_service(user: User, process: str = None):
    CLIENT_SECRET_FILE = settings.CLIENT_SECRET_FILE
    API_SERVICE_NAME = settings.API_NAME
    API_VERSION = settings.API_VERSION
    SCOPES = ['https://www.googleapis.com/auth/drive']

    cred = None
    pickle_file = os.path.join(settings.GOOGLE_DRIVE_CONFIG_ROOT, f'token_{API_SERVICE_NAME}_{API_VERSION}_email_{user.email}.pickle')
    isFileExist = os.path.exists(pickle_file)

    if isFileExist:
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)
    
    if not isFileExist and process == 'cron': return False

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server(port=8080)

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None