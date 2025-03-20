import pandas as pd

class DataAnalyzer:
    def analyze_data(self, df):
        print("[INFO] Iniciando análisis de datos...")
        if df is None or df.empty:
            print("[ERROR] No hay datos para analizar.")
            return None

        try:
            summary = df.describe()
            missing_values = df.isnull().sum()
            unique_counts = df.nunique()

            print("[INFO] Análisis completado.")
            return {
                "summary": summary,
                "missing_values": missing_values,
                "unique_counts": unique_counts
            }
        except Exception as e:
            print(f"[ERROR] Ocurrió un problema durante el análisis de datos: {e}")
            return None
