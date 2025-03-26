import pandas as pd
import numpy as np
import os

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


# --- NUEVA FUNCIÓN DE LIMPIEZA ---
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Versión mejorada con:
    - Validación estricta de códigos
    - Formateo consistente de decimales
    - Filtrado robusto de filas inválidas
    """
    df_clean = df.copy()

    # 1. Limpieza básica (strings)
    for col in ['codigo', 'nombre', 'categoria', 'ubicacion']:
        df_clean[col] = df_clean[col].astype(str).str.strip()

    # 2. Normalización CRÍTICA de códigos (PR + 3-4 dígitos)
    df_clean['codigo'] = (
        df_clean['codigo']
        .str.upper()
        .str.extract(r'(PR?\s?(\d{3,4}))')[0]  # Captura PR + 3-4 dígitos
        .str.replace(r'\D', '', regex=True)  # Elimina caracteres no numéricos
        .apply(lambda x: f"PR{x.zfill(3)}" if pd.notna(x) and x.isdigit() else pd.NA)
    )

    # 3. Filtrado de filas sin código válido (¡Nuevo!)
    df_clean = df_clean.dropna(subset=['codigo'])

    # 4. Limpieza numérica con control estricto
    df_clean['cantidad'] = (
        pd.to_numeric(df_clean['cantidad'], errors='coerce')
        .abs()
        .fillna(0)
        .astype(int)
    )
    df_clean['precio'] = (
        pd.to_numeric(df_clean['precio'], errors='coerce')
        .abs()
        .round(2)
    )

    # 5. Cálculo preciso de valor_total
    df_clean['valor_total'] = (
            df_clean['cantidad'] * df_clean['precio']
    ).round(2)  # ¡Redondeo crítico aquí!

    # 6. Filtrado final (asegura todas las columnas clave)
    df_clean = df_clean[
        (df_clean['cantidad'] > 0) &
        (df_clean['precio'] > 0) &
        (df_clean['nombre'].str.len() > 3)
        ].drop_duplicates(subset=['codigo', 'nombre'])

    # 7. Ordenamiento por código (¡Nuevo!)
    df_clean = df_clean.sort_values('codigo').reset_index(drop=True)

    # Reporte mejorado
    print("\n=== REPORTE FINAL ===")
    print(f"Registros válidos: {len(df_clean)}")
    print(f"Valor total: ${df_clean['valor_total'].sum():,.2f}")
    print("\n5 primeros registros:")
    print(df_clean.head().to_string(index=False))

    return df_clean


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
        df = clean_data(df)  # Sobreescribimos df con la versión limpia

        print("\nInventario cargado y limpiado...")
        # show_all_products()
        #filter_product_by_code()
        #filter_product_by_name()
        #calculate_inventory_value(df)

        # Opcional: Guardar versión limpia
        clean_path = full_path.replace('.csv', '_clean.csv')
        df.to_csv(clean_path, index=False)
        print(f"\nVersión limpia guardada en: {clean_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")