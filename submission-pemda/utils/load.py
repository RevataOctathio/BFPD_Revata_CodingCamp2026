import pandas as pd
from sqlalchemy import create_engine
from googleapiclient.discovery import build
from google.oauth2 import service_account

def load_to_csv(df, file_name='products.csv'):
    try:
        df.to_csv(file_name, index=False)
        print(f"===Sukses CSV: {file_name}===")
        return True
    except Exception as e:
        print(f"===Error CSV: {e}===")
        return False

def load_to_google_sheets(df, spreadsheet_id, json_key_path):
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(json_key_path, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)
        values = [df.columns.values.tolist()] + df.values.tolist()
        service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range='Sheet1!A1', body={}).execute()
        service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range='Sheet1!A1', valueInputOption='RAW', body={'values': values}).execute()
        print("===Sukses Google Sheets===")
        return True
    except Exception as e:
        print(f"===Error Google Sheets: {e}===")
        return False

def load_to_postgresql(df, db_config):
    try:
        conn_url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        engine = create_engine(conn_url)
        df.to_sql('fashion_products', engine, if_exists='replace', index=False)
        print("===Sukses PostgreSQL=== ")
        return True
    except Exception as e:
        print(f"===Error PostgreSQL: {e}===")
        return False