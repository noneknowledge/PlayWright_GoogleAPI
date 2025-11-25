from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pandas as pd

import os

# Tạo thư mục "data", nếu đã có thì bỏ qua
os.makedirs("data", exist_ok=True)


# ID của Google Sheets từ URL
SPREADSHEET_ID = '1lNsIW2A1gmurYZ-DJt65xuX_yEsxyvoqPx84Q2B8rEM'
RANGE_NAME = 'A2:Z2'  # Dòng đầu tiên, từ cột A đến Z

# Tạo credentials từ file JSON
creds = service_account.Credentials.from_service_account_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)
# creds.refresh(Request())
# print (creds.token)

# Tạo service để gọi API
service = build('sheets', 'v4', credentials=creds)

# Gọi API để lấy dữ liệu
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

# In kết quả
if not values:
    print("Không có dữ liệu.")
else:
    firstRow= values[0]
    print("Dòng đầu tiên:", firstRow[0])

    
    data = {"Name":firstRow[0],"Email":firstRow[1],"Content":firstRow[2]}
    df = pd.DataFrame(data,index=[0])
    
    df.to_csv('data/basic.csv',index=0)
    df.to_json("data/basic.json",index=0)

    print("End.")


