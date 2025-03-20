import pandas as pd
import os
import re


class DataCleaner:
    def clean_data(self, df):
        print("[INFO] Iniciando limpieza de datos...")
        if df is None or df.empty:
            print("[ERROR] No hay datos para limpiar.")
            return None

        try:
            # Crear directorio para reportes si no existe
            os.makedirs("reports", exist_ok=True)
            error_log_path = "reports/error_log.txt"

            # Eliminar filas completamente vacías
            df.dropna(how='all', inplace=True)

            # Guardar filas corruptas antes de limpiarlas
            corrupted_rows = df[df.isnull().sum(axis=1) > (df.shape[1] * 0.5)]  # Si más del 50% de la fila es NaN
            with open(error_log_path, "w", encoding="utf-8") as log_file:
                log_file.write("[INFO] Filas corruptas detectadas y eliminadas:\n")
                log_file.write(corrupted_rows.to_string())

            # Eliminar filas corruptas
            df.dropna(thresh=int(df.shape[1] * 0.5), inplace=True)  # Mantener filas con al menos 50% de datos válidos

            # Rellenar valores nulos con 0
            df = df.infer_objects(copy=False)
            df.fillna(0, inplace=True)

            # Normalizar nombres de columnas
            df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

            # Renombrar columnas clave para estandarizar los nombres
            column_mapping = {
                "nombre_producto": "producto",
                "precio_unitario": "precio_unitario",
                "cantidad": "cantidad_en_stock"
            }
            df.rename(columns=column_mapping, inplace=True)

            # Convertir columnas numéricas correctamente
            numeric_cols = ['cantidad_en_stock', 'precio_unitario']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Eliminar caracteres extraños en los datos
            df = df.map(lambda x: re.sub(r'[^a-zA-Z0-9 .,]', '', str(x)) if isinstance(x, str) else x)

            print(f"[INFO] Datos limpiados: {df.shape[0]} filas, {df.shape[1]} columnas.")
            return df
        except Exception as e:
            print(f"[ERROR] Ocurrió un problema durante la limpieza de datos: {e}")
            return None
