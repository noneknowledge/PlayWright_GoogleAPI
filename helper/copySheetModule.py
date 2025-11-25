from google.oauth2 import service_account
from googleapiclient.discovery import build

def copySheet():
    # 1. Khởi tạo credentials từ service account
    SERVICE_ACCOUNT_FILE = "./credentials.json"
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)

    # 2. ID của file Spreadsheet gốc
    FILE_ID = "1lNsIW2A1gmurYZ-DJt65xuX_yEsxyvoqPx84Q2B8rEM"

    # 3. Xuất file dưới dạng Excel (.xlsx)
    request = service.files().export_media(
        fileId=FILE_ID,
        mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # 4. Ghi ra file trên máy
    with open("data/copySheet.xlsx", "wb") as f:
        f.write(request.execute())


