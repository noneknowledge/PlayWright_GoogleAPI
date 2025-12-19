from google.oauth2 import service_account
from googleapiclient.discovery import build
import os, hashlib
from dotenv import dotenv_values


config = dotenv_values(".env")

# 1. Xác thực bằng Service Account
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

# 2. Hàm tạo thư mục nếu chưa có
def ensure_folder(service, name, parent_id=None):
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(
        q=query,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        corpora="allDrives",
        fields="files(id, name)"
    ).execute()
    items = results.get('files', [])
    if items:
        return items[0]['id']
    # tạo mới
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]
    folder = service.files().create(
        body=file_metadata,
        fields='id',
        supportsAllDrives=True
    ).execute()
    return folder['id']

# 3. Hàm tính md5
def md5sum(filename):
    h = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

# 4. Upload file nếu chưa có
def upload_if_needed(service, local_path, drive_folder_id, mode="name+md5"):
    filename = os.path.basename(local_path)
    query = f"name='{filename}' and '{drive_folder_id}' in parents and trashed=false"
    results = service.files().list(
        q=query,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
        corpora="allDrives",
        fields="files(id, name, md5Checksum)"
    ).execute()
    items = results.get('files', [])
    if items:
        if mode == "name":
            return items[0]['id']
        elif mode == "name+md5":
            local_md5 = md5sum(local_path)
            if items[0].get('md5Checksum') == local_md5:
                return items[0]['id']
    # upload mới
    from googleapiclient.http import MediaFileUpload
    file_metadata = {'name': filename, 'parents': [drive_folder_id]}
    media = MediaFileUpload(local_path, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True
    ).execute()
    return file['id']

def mirror_folder(service, local_root, drive_parent_id, mode="name+md5"):
    for root, dirs, files in os.walk(local_root):
        rel_path = os.path.relpath(root, local_root)
      
        if rel_path == ".":
            current_drive_id = drive_parent_id
        else:
            parts = rel_path.split(os.sep)
            current_drive_id = drive_parent_id
            for p in parts:
                current_drive_id = ensure_folder(service, p, parent_id=current_drive_id)

        for f in files:
            local_path = os.path.join(root, f)
            upload_if_needed(service, local_path, current_drive_id, mode=mode)


# 5. Mirror thư mục Downloads
base_dir = os.path.dirname(__file__)
local_download = os.path.join(base_dir, "downloads")
target_parent_id = config["TARGET_PARENT_ID"]
drive_folder_id = ensure_folder(service, "DownloadsMirror", parent_id=target_parent_id)


mirror_folder(service, local_download, target_parent_id)