import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_service():
    """Erstellt einen Google Drive API-Service."""
    creds = None
    auth_dir = 'auth'
    token_path = os.path.join(auth_dir, 'token.pickle')
    creds_path = os.path.join(auth_dir, 'credentials.json')
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
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
    
def find_missing_files(service, folder_id, file_list):
    """Vergleicht die Dateinamen und IDs in einer Liste mit den Dateien in einem Google Drive-Ordner
    und gibt ein Dictionary mit den Namen und IDs der Dateien zurück, die im Google Drive vorhanden sind,
    aber nicht in der Liste."""
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name)"
    ).execute()
    
    drive_files = results.get('files', [])
    
    file_list_dict = {file[1]: file[0] for file in file_list}
    
    missing_files = {}

    for file in drive_files:
        file_id = file['id']
        file_name = file['name']
        if file_id not in file_list_dict:
            missing_files[file_name] = file_id

    return missing_files

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

def download_missing_files(service, missing_files_dict, download_folder):
    """Lädt alle Dateien herunter, die in missing_files_dict angegeben sind und speichert sie im angegebenen Ordner."""
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for file_name, file_id in missing_files_dict.items():
        request = service.files().get_media(fileId=file_id)
        file_path = os.path.join(download_folder, file_name)

        with open(file_path, 'wb') as file:
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    print(f"Download {int(status.progress() * 100)}% für {file_name}.")
            print(f"{file_name} wurde erfolgreich heruntergeladen und gespeichert in {file_path}.")

def main(file_list, download_folder="Audios"):
    """Hauptfunktion zur Ausführung des Skripts."""
    service = get_service()
    folder_name = "Audio Upload"
    folder_id = get_folder_id(service, folder_name)
    
    if folder_id:
        # list_files_in_folder(service, folder_id)
        # return {}
        missing_files = find_missing_files(service, folder_id, file_list)
        download_missing_files(service, missing_files_dict=missing_files, download_folder=download_folder)
        return missing_files
    else:
        return {}