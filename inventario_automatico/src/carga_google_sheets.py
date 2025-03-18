import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def autenticar_google_sheets():
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("config/credentials.json", SCOPES)
        cliente = gspread.authorize(creds)
        return cliente
    except Exception as e:
        print(f"⚠️ Error en la autenticación de Google Sheets: {e}")
        return None

def cargar_desde_google_sheets(sheet_id, sheet_name="Sheet1"):
    try:
        cliente = autenticar_google_sheets()
        if not cliente:
            raise ConnectionError("No se pudo conectar a Google Sheets.")

        sheet = cliente.open_by_key(sheet_id).worksheet(sheet_name)
        datos = sheet.get_all_records()
        df = pd.DataFrame(datos)
        return df
    except Exception as e:
        print(f"⚠️ Error al cargar datos desde Google Sheets: {e}")
        return None
