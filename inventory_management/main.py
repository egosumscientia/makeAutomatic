from scripts import data_analysis, data_clean, data_load
import os

# Configuración de rutas
DATA_PATH = "/home/pauloenrique/Documents/makeAutomatic/inventory_management/data"
BASE_NAME = "inventario"  # Nombre base sin extensión


def main():
    print("Welcome Paulo Enrique!")
    print("Cargando inventario...")

    try:
        # Intenta cargar primero .ods, luego busca alternativas
        df = data_load.load_data(f"{DATA_PATH}/{BASE_NAME}.ods")

        print("\n✅ Inventario cargado exitosamente")
        print("Muestra de datos originales:")
        print(df.head(3))

        # Limpieza de datos
        df = data_clean.data_clean(df)
        print("\n🧹 Datos limpiados correctamente")

        # Análisis
        print("\n📊 === EJECUTANDO ANÁLISIS AVANZADO ===")
        data_analysis.analizar_inventario(df)

        # Guardado automático con la misma extensión del archivo cargado
        actual_file_path = data_load.find_actual_file_path(f"{DATA_PATH}/{BASE_NAME}")
        file_ext = os.path.splitext(actual_file_path)[1]
        clean_path = f"{DATA_PATH}/{BASE_NAME}_clean{file_ext}"

        if file_ext == '.csv':
            df.to_csv(clean_path, index=False)
        else:
            df.to_excel(clean_path, index=False)

        print(f"\n💾 Versión limpia guardada en: {clean_path}")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
    except ValueError as e:
        print(f"\n❌ Error en los datos: {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()