import pytest
import pandas as pd
import os
from makeAutomatic.inventario_automatico.src.carga_datos import detectar_tipo_archivo, cargar_desde_dropbox, cargar_desde_s3, cargar_desde_google_drive
from makeAutomatic.inventario_automatico.src.carga_google_sheets import cargar_desde_google_sheets

# Directorio base de los archivos de prueba
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Variables de configuración (Se piden si no están en .env)
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID_TEST") or input("🔹 Ingrese el ID del Google Sheet de prueba: ").strip()
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME_TEST", "Inventario")

GOOGLE_DRIVE_FILE_ID = os.getenv("GOOGLE_DRIVE_FILE_ID_TEST") or input("🔹 Ingrese el ID del archivo en Google Drive de prueba: ").strip()
DROPBOX_URL = os.getenv("DROPBOX_URL_TEST") or input("🔹 Ingrese el enlace de Dropbox de prueba: ").strip()

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME_TEST") or input("🔹 Ingrese el nombre del bucket S3 de prueba: ").strip()
S3_FILE_KEY = os.getenv("S3_FILE_KEY_TEST") or input("🔹 Ingrese la clave del archivo en S3 de prueba: ").strip()
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_TEST") or input("🔹 Ingrese la AWS Access Key de prueba: ").strip()
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY_TEST") or input("🔹 Ingrese la AWS Secret Key de prueba: ").strip()

@pytest.mark.parametrize("archivo", [
    os.path.join(DATA_DIR, "inventario.xlsx"),
    os.path.join(DATA_DIR, "inventario.csv"),
    os.path.join(DATA_DIR, "inventario.ods")
])
def test_cargar_archivo_local(archivo):
    """ Prueba la carga de archivos locales en diferentes formatos """
    df = detectar_tipo_archivo(archivo)
    assert df is not None, f"⚠️ Error al cargar archivo {archivo}"
    assert isinstance(df, pd.DataFrame), "El archivo cargado no es un DataFrame"

def test_cargar_desde_google_sheets():
    """ Prueba la carga de datos desde Google Sheets """
    df = cargar_desde_google_sheets(GOOGLE_SHEET_ID, GOOGLE_SHEET_NAME)
    assert df is not None, "⚠️ Error al cargar desde Google Sheets"
    assert isinstance(df, pd.DataFrame), "Los datos de Google Sheets no son un DataFrame"

def test_cargar_desde_google_drive():
    """ Prueba la carga de datos desde Google Drive """
    df = cargar_desde_google_drive(GOOGLE_DRIVE_FILE_ID)
    assert df is not None, "⚠️ Error al cargar desde Google Drive"
    assert isinstance(df, pd.DataFrame), "Los datos de Google Drive no son un DataFrame"

def test_cargar_desde_dropbox():
    """ Prueba la carga de datos desde Dropbox """
    df = cargar_desde_dropbox(DROPBOX_URL)
    assert df is not None, "⚠️ Error al cargar desde Dropbox"
    assert isinstance(df, pd.DataFrame), "Los datos de Dropbox no son un DataFrame"

def test_cargar_desde_s3():
    """ Prueba la carga de datos desde AWS S3 """
    df = cargar_desde_s3(S3_BUCKET_NAME, S3_FILE_KEY, AWS_ACCESS_KEY, AWS_SECRET_KEY)
    assert df is not None, "⚠️ Error al cargar desde S3"
    assert isinstance(df, pd.DataFrame), "Los datos de S3 no son un DataFrame"
