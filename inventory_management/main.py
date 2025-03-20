import os
from scripts.data_loader import DataLoader
from scripts.data_cleaner import DataCleaner
from scripts.data_analyzer import DataAnalyzer
from scripts.data_visualizer import DataVisualizer


def main():
    print("Iniciando el sistema de gestión de inventario...")
    data_folder = "data"

    if not os.path.exists(data_folder):
        print(f"[ERROR] La carpeta de datos '{data_folder}' no existe.")
        return

    # Cargar los datos
    print("Cargando datos...")
    loader = DataLoader()
    data = loader.load_data(data_folder)
    if data is None or data.empty:
        print("[ERROR] No se encontraron datos válidos en la carpeta de datos.")
        return
    print("Datos cargados exitosamente.")

    # Limpiar los datos
    print("Limpiando datos...")
    cleaner = DataCleaner()
    clean_data = cleaner.clean_data(data)
    print(f"Datos limpiados: {clean_data.shape[0]} filas, {clean_data.shape[1]} columnas.")

    # Analizar los datos
    print("Analizando datos...")
    analyzer = DataAnalyzer()
    analysis_results = analyzer.analyze_data(clean_data)
    if not analysis_results:
        print("[ERROR] No se pudo realizar el análisis de datos.")
        return
    print("Análisis completado.")

    # Visualizar los datos
    print("Generando visualizaciones...")
    visualizer = DataVisualizer()
    visualizer.generate_visuals(analysis_results, clean_data)  # Se pasa clean_data correctamente
    print("Gráficos generados en la carpeta 'reports/'.")


if __name__ == "__main__":
    main()
