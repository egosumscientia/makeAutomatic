import matplotlib.pyplot as plt

def analizar_inventario(df):
    """ Analiza el inventario, agregando estados de stock """
    try:
        if df is None or df.empty:
            raise ValueError("El DataFrame está vacío o no se pudo cargar.")

        df["Estado"] = df.apply(lambda row: "BAJO STOCK" if row["Stock Actual"] <= row["Stock Mínimo"] and row["Stock Actual"] > 0
                                else "AGOTADO" if row["Stock Actual"] == 0
                                else "STOCK SUFICIENTE", axis=1)
        return df
    except Exception as e:
        print(f"⚠️ Error en el análisis del inventario: {e}")
        return None

def generar_grafico(df, output_file):
    """ Genera un gráfico de barras mostrando el estado del inventario """
    try:
        if df is None or df.empty:
            raise ValueError("No se pueden generar gráficos porque el DataFrame está vacío.")

        # Contar la cantidad de productos en cada estado
        conteo_estado = df["Estado"].value_counts()

        # Crear el gráfico de barras
        plt.figure(figsize=(8, 5))
        plt.bar(conteo_estado.index, conteo_estado.values, color=['green', 'orange', 'red'])
        plt.xlabel("Estado del Inventario")
        plt.ylabel("Cantidad de Productos")
        plt.title("Distribución del Inventario por Estado")
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Guardar gráfico
        plt.savefig(output_file)
        plt.close()
        print(f"✅ Gráfico guardado en {output_file}")

    except Exception as e:
        print(f"⚠️ Error al generar gráfico: {e}")
