from flask import Flask, request
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'key.json'

RAG_DOC_ID = os.environ.get('RAG_DOC_ID')
SCHEDULE_SHEET_ID = os.environ.get('SCHEDULE_SHEET_ID')

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

@app.route('/')
def home():
    return 'Сервер работает'

@app.route('/webhook/schedule', methods=['POST'])
def handle_schedule_update():
    print("Расписание изменилось, скачиваем XLSX...")
    drive_service = get_drive_service()
    xlsx_content = drive_service.files().export(
        fileId=SCHEDULE_SHEET_ID,
        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ).execute()
    print(f"Скачано {len(xlsx_content)} байт")
    # TODO: здесь будет парсинг и обновление базы
    return 'OK', 200

@app.route('/webhook/rag', methods=['POST'])
def handle_rag_update():
    print("RAG-документ изменился, скачиваем DOCX...")
    drive_service = get_drive_service()
    docx_content = drive_service.files().export(
        fileId=RAG_DOC_ID,
        mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ).execute()
    print(f"Скачано {len(docx_content)} байт")
    # TODO: здесь будет обновление векторной базы
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
