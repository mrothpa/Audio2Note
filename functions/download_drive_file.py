from __future__ import print_function
import os.path
import pickle
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Benötigte SCOPES für den Zugriff auf Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def get_service():
    """Erstellt einen Google Drive API-Service."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def list_files_in_folder(service, folder_id):
    """Listet alle Dateien in einem Ordner auf."""
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('Keine Dateien gefunden.')
    else:
        for item in items:
            print(f"Dateiname: {item['name']}, ID: {item['id']}")

def get_folder_id(service, folder_name):
    """Holt die Ordner-ID anhand des Ordnernamens."""
    results = service.files().list(
        q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)").execute()
    items = results.get('files', [])
    
    if items:
        return items[0]['id']
    else:
        print(f"Ordner '{folder_name}' nicht gefunden.")
        return None

def list_my_drive_files(service):
    """Listet alle Dateien in 'Meine Ablage' auf."""
    results = service.files().list(
        q="'root' in parents",
        fields="files(id, name)").execute()
    items = results.get('files', [])
    
    if not items:
        print('Keine Dateien in "Meine Ablage" gefunden.')
    else:
        for item in items:
            print(f"Dateiname: {item['name']}, ID: {item['id']}")

def main():
    # Erstelle den API-Service
    service = get_service()

    # Liste Dateien im Ordner "Audio Upload"
    folder_name = "Audio Upload"
    folder_id = get_folder_id(service, folder_name)
    
    if folder_id:
        print(f"Dateien im Ordner '{folder_name}':")
        list_files_in_folder(service, folder_id)
        print("\n")

    # Liste Dateien in "Meine Ablage"
    print('Dateien in "Meine Ablage":')
    list_my_drive_files(service)

if __name__ == '__main__':
    main()
