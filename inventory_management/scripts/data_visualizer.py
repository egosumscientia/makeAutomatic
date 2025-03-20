import matplotlib.pyplot as plt
import os

class DataVisualizer:
    def generate_visuals(self, analysis_results, df):
        print("[INFO] Generando visualizaciones...")
        if analysis_results is None or df is None:
            print("[ERROR] No hay datos para visualizar.")
            return

        output_dir = "reports"
        os.makedirs(output_dir, exist_ok=True)

        try:
            summary = analysis_results.get("summary")
            if summary is not None:
                summary.plot(kind='bar')
                plt.title("Resumen Estadístico del Inventario")
                plt.savefig(os.path.join(output_dir, "summary.png"))
                plt.close()
                print("[INFO] Gráfico 'summary.png' guardado.")

            missing_values = analysis_results.get("missing_values")
            if missing_values is not None:
                missing_values.plot(kind='bar', color='red')
                plt.title("Valores Faltantes")
                plt.savefig(os.path.join(output_dir, "missing_values.png"))
                plt.close()
                print("[INFO] Gráfico 'missing_values.png' guardado.")

            unique_counts = analysis_results.get("unique_counts")
            if unique_counts is not None:
                unique_counts.plot(kind='bar', color='green')
                plt.title("Cantidad de Valores Únicos")
                plt.savefig(os.path.join(output_dir, "unique_counts.png"))
                plt.close()
                print("[INFO] Gráfico 'unique_counts.png' guardado.")

            # Verificar si la columna 'producto' existe antes de generar gráficos
            if 'producto' in df.columns and 'cantidad_en_stock' in df.columns:
                low_stock = df[df['cantidad_en_stock'] < 10]
                if not low_stock.empty:
                    low_stock.plot(x='producto', y='cantidad_en_stock', kind='bar', color='orange')
                    plt.title("Productos con Bajo Stock")
                    plt.savefig(os.path.join(output_dir, "low_stock.png"))
                    plt.close()
                    print("[INFO] Gráfico 'low_stock.png' guardado.")

            # Nuevo: Distribución del stock
            if 'cantidad_en_stock' in df.columns:
                df['cantidad_en_stock'].hist(bins=20, color='blue', alpha=0.7)
                plt.title("Distribución de Stock")
                plt.xlabel("Cantidad en Stock")
                plt.ylabel("Frecuencia")
                plt.savefig(os.path.join(output_dir, "stock_distribution.png"))
                plt.close()
                print("[INFO] Gráfico 'stock_distribution.png' guardado.")

            # Nuevo: Valor total del inventario
            if 'producto' in df.columns and 'precio_unitario' in df.columns and 'cantidad_en_stock' in df.columns:
                df['valor_total'] = df['cantidad_en_stock'] * df['precio_unitario']
                df.sort_values('valor_total', ascending=False).head(10).plot(x='producto', y='valor_total', kind='bar', color='purple')
                plt.title("Valor Total del Inventario")
                plt.savefig(os.path.join(output_dir, "inventory_value.png"))
                plt.close()
                print("[INFO] Gráfico 'inventory_value.png' guardado.")

            print("[INFO] Visualizaciones generadas correctamente.")
        except Exception as e:
            print(f"[ERROR] No se pudieron generar algunos gráficos: {e}")
