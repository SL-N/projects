from future import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Айдишник таблицы и лист который он будет парсить, после восклицательного знака идет размерность - с какой по какую ячейку будет парситься
#Если хочешь со всем эти поиграться, то смотри ссылку в трелло, потому что надо сначала подключиться к сервисам гугла, чтобы это все работало
SAMPLE_SPREADSHEET_ID = '1DHir9K8KO8a2AX3AfPiE422HXgf_7AKgSOSS-UOMt_A'
SAMPLE_RANGE_NAME = 'Раписание 1 полугодие 2020/2021!C3:BG42'

def main():
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        for row in values:
         # Выводит расписание у первой группы без пустых строчек row[0] отвечает за время, row[1,2 и т.д за группы]
            if(row[1] != ""):
                print('%s' % (row[1]))

if name == 'main':
    main()
