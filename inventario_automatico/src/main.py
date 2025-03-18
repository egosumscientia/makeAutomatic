from .carga_google_sheets import cargar_desde_google_sheets
from .carga_datos import cargar_desde_google_drive, cargar_desde_dropbox, cargar_desde_s3
from .analitica import analizar_inventario
from .exportacion import (
    exportar_a_excel, exportar_a_ods, exportar_a_odt,
    exportar_a_pdf, exportar_a_docx, exportar_a_txt
)

from ..config.settings import FUENTE_DATOS, GOOGLE_SHEET_ID, GOOGLE_SHEET_NAME
from ..config.settings import GOOGLE_DRIVE_FILE_ID, DROPBOX_URL, S3_BUCKET_NAME, S3_FILE_KEY, AWS_ACCESS_KEY, AWS_SECRET_KEY

df = None

if FUENTE_DATOS == "google_sheets":
    df = cargar_desde_google_sheets(GOOGLE_SHEET_ID, GOOGLE_SHEET_NAME)
elif FUENTE_DATOS == "google_drive":
    df = cargar_desde_google_drive(GOOGLE_DRIVE_FILE_ID)
elif FUENTE_DATOS == "dropbox":
    df = cargar_desde_dropbox(DROPBOX_URL)
elif FUENTE_DATOS == "s3":
    df = cargar_desde_s3(S3_BUCKET_NAME, S3_FILE_KEY, AWS_ACCESS_KEY, AWS_SECRET_KEY)

if df is not None:
    df = analizar_inventario(df)
    if df is not None:
        exportar_a_excel(df, "data/reportes/Reporte_Inventario.xlsx")
        exportar_a_ods(df, "data/reportes/Reporte_Inventario.ods")
        exportar_a_odt(df, "data/reportes/Reporte_Inventario.odt")
        exportar_a_pdf(df, "data/reportes/Reporte_Inventario.pdf")
        exportar_a_docx(df, "data/reportes/Reporte_Inventario.docx")
        exportar_a_txt(df, "data/reportes/Reporte_Inventario.txt")
