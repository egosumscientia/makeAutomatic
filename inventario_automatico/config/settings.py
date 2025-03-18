import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# Fuente de datos (no debe estar quemada, se pedirá si no está configurada)
FUENTES_VALIDAS = ["google_sheets", "google_drive", "dropbox", "s3", "local"]
FUENTE_DATOS = os.getenv("FUENTE_DATOS")

if FUENTE_DATOS not in FUENTES_VALIDAS:
    FUENTE_DATOS = input(f"🔹 Ingrese la fuente de datos {FUENTES_VALIDAS}: ").strip()

# Google Sheets (Se pide si no está en .env)
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
if not GOOGLE_SHEET_ID:
    GOOGLE_SHEET_ID = input("🔹 Ingrese el ID del Google Sheet: ").strip()

GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Inventario")

# Google Drive
GOOGLE_DRIVE_FILE_ID = os.getenv("GOOGLE_DRIVE_FILE_ID")
if not GOOGLE_DRIVE_FILE_ID and FUENTE_DATOS == "google_drive":
    GOOGLE_DRIVE_FILE_ID = input("🔹 Ingrese el ID del archivo en Google Drive: ").strip()

# Dropbox
DROPBOX_URL = os.getenv("DROPBOX_URL")
if not DROPBOX_URL and FUENTE_DATOS == "dropbox":
    DROPBOX_URL = input("🔹 Ingrese el enlace de Dropbox: ").strip()

# AWS S3
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_FILE_KEY = os.getenv("S3_FILE_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

if FUENTE_DATOS == "s3":
    if not S3_BUCKET_NAME:
        S3_BUCKET_NAME = input("🔹 Ingrese el nombre del bucket S3: ").strip()
    if not S3_FILE_KEY:
        S3_FILE_KEY = input("🔹 Ingrese la clave del archivo en S3: ").strip()
    if not AWS_ACCESS_KEY:
        AWS_ACCESS_KEY = input("🔹 Ingrese la AWS Access Key: ").strip()
    if not AWS_SECRET_KEY:
        AWS_SECRET_KEY = input("🔹 Ingrese la AWS Secret Key: ").strip()
