import pandas as pd


class DataCleaner:
    def clean_data(self, df):
        print("[INFO] Iniciando limpieza de datos...")
        if df is None or df.empty:
            print("[ERROR] No hay datos para limpiar.")
            return None

        try:
            df.dropna(how='all', inplace=True)
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

            # Convertir listas en strings
            for col in df.columns:
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)

            print(f"[INFO] Datos limpiados: {df.shape[0]} filas, {df.shape[1]} columnas.")
            return df
        except Exception as e:
            print(f"[ERROR] Ocurrió un problema durante la limpieza de datos: {e}")
            return None
