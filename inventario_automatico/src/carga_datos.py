import pandas as pd
import os
import requests
import boto3
from io import BytesIO
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Autenticación con Google Drive
try:
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
except Exception as e:
    print(f"⚠️ Error en la autenticación de Google Drive: {e}")
    drive = None


def detectar_tipo_archivo(ruta_archivo):
    """ Detecta automáticamente el tipo de archivo y lo carga en un DataFrame """
    try:
        ext = os.path.splitext(ruta_archivo)[-1].lower()

        if ext in [".xlsx", ".xls"]:
            df = pd.read_excel(ruta_archivo, engine="openpyxl")
        elif ext == ".csv":
            df = pd.read_csv(ruta_archivo, encoding="utf-8")
        elif ext == ".ods":
            df = pd.read_excel(ruta_archivo, engine="odf")
        else:
            raise ValueError(f"⚠️ Formato de archivo no soportado: {ext}")

        return df
    except Exception as e:
        print(f"⚠️ Error al cargar archivo {ruta_archivo}: {e}")
        return None


def cargar_desde_google_drive(file_id):
    """ Descarga un archivo desde Google Drive y lo carga en Pandas """
    try:
        if drive is None:
            raise ConnectionError("No se pudo conectar a Google Drive.")

        file = drive.CreateFile({'id': file_id})
        file.GetContentFile("archivo_google_drive.xlsx")
        return detectar_tipo_archivo("archivo_google_drive.xlsx")
    except Exception as e:
        print(f"⚠️ Error al cargar desde Google Drive: {e}")
        return None


def cargar_desde_dropbox(url):
    """ Descarga un archivo desde Dropbox usando un enlace compartido """
    try:
        if "dl=0" in url:
            url = url.replace("dl=0", "dl=1")
        response = requests.get(url)
        response.raise_for_status()
        return detectar_tipo_archivo(BytesIO(response.content))
    except Exception as e:
        print(f"⚠️ Error al cargar desde Dropbox: {e}")
        return None


def cargar_desde_s3(bucket_name, file_key, aws_access_key, aws_secret_key):
    """ Descarga un archivo desde AWS S3 y lo carga en Pandas """
    try:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        return detectar_tipo_archivo(BytesIO(obj['Body'].read()))
    except Exception as e:
        print(f"⚠️ Error al cargar desde AWS S3: {e}")
        return None
