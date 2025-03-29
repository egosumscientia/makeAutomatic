import pandas as pd
import numpy as np
import os
from scripts import data_analysis
from scripts import data_clean

data_path = "/home/pauloenrique/Documents/makeAutomatic/inventory_management/data"
file_name = "inventario.csv"
full_path = f"{data_path}/{file_name}"
df = None


# --- FUNCIONES EXISTENTES (sin cambios) ---
def show_all_products():
    print("El siguiente es el contenido completo del archivo cargado: ")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    print(df)


def filter_product_by_code():
    producto = df[df['codigo'] == 'PR100']
    print(f"Busqueda por codigo: {producto}")


def filter_product_by_name():
    producto = df[df['nombre'] == 'LED UTP']
    print(f"Busqueda por nombre: {producto}")


def calculate_inventory_value(df: pd.DataFrame) -> None:
    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
    df['valor_total'] = df['cantidad'] * df['precio']
    print("VALOR TOTAL ($)")
    print(df['valor_total'].sum())


# --- EJECUCIÓN PRINCIPAL (modificada) ---
if __name__ == "__main__":
    print(f"Welcome Paulo Enrique!")
    print("Cargando inventario...")

    try:
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"El archivo {full_path} no existe")

        print("Archivo encontrado. Leyendo...")
        df = pd.read_csv(full_path)
        print("\nMuestra de datos originales:")
        print(df.head(3))

        # --- NUEVO: Proceso de limpieza ---
        df = data_clean.data_clean(df)  # Sobreescribimos df con la versión limpia

        print("\nInventario cargado y limpiado...")
        # show_all_products()
        #filter_product_by_code()
        #filter_product_by_name()
        #calculate_inventory_value(df)

        # --- INTEGRACIÓN DE data_analysis.py ---
        print("\n=== EJECUTANDO ANÁLISIS AVANZADO ===")
        data_analysis.analizar_inventario(df)  # Llamada a la función principal

        # Opcional: Guardar versión limpia
        clean_path = full_path.replace('.csv', '_clean.csv')
        df.to_csv(clean_path, index=False)
        print(f"\nVersión limpia guardada en: {clean_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")