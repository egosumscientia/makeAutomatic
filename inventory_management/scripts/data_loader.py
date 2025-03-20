import os
import pandas as pd
import zipfile
import pyexcel_ods
import rarfile


class DataLoader:
    def load_data(self, path):
        print("[INFO] Iniciando carga de datos...")
        data_frames = []

        if not os.path.exists(path):
            print(f"[ERROR] La ruta {path} no existe.")
            return None

        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if file.endswith(".csv"):
                        df = pd.read_csv(file_path)
                    elif file.endswith(".xlsx"):
                        df = pd.read_excel(file_path)
                    elif file.endswith(".ods"):
                        df = pd.DataFrame(pyexcel_ods.get_data(file_path))
                    elif file.endswith(".zip"):
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(path)
                            return self.load_data(path)
                    elif file.endswith(".rar"):
                        with rarfile.RarFile(file_path, 'r') as rar_ref:
                            rar_ref.extractall(path)
                            return self.load_data(path)
                    else:
                        print(f"[WARNING] Formato no soportado: {file}")
                        continue

                    data_frames.append(df)
                    print(f"[INFO] Archivo {file} cargado con éxito.")
                except Exception as e:
                    print(f"[ERROR] No se pudo cargar {file}: {e}")

        if data_frames:
            print("[INFO] Datos cargados correctamente.")
            return pd.concat(data_frames, ignore_index=True)
        else:
            print("[ERROR] No se encontraron archivos válidos.")
            return None