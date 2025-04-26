import openai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from googleapiclient.http import MediaFileUpload

# OpenAIのAPIキーをセット
openai.api_key = 'YOUR_OPENAI_API_KEY'  # ここにOpenAIのAPIキーを入力

# Google API認証とサービスの設定
def authenticate_google_drive():
    creds = None
    # トークンファイルがある場合は、Google APIの認証を自動化
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive.readonly'])
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', ['https://www.googleapis.com/auth/drive.readonly'])
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

# ChatGPTとのインタラクション
def query_chatgpt(prompt):
    response = openai.Completion.create(
      engine="text-davinci-003",  # 最新のモデルに変更可能
      prompt=prompt,
      max_tokens=150
    )
    return response.choices[0].text.strip()

# Google Driveにファイルをアップロードする関数
def upload_file_to_drive(file_path):
    drive_service = authenticate_google_drive()
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

