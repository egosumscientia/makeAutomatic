import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def analizar_inventario(df):
    """
    Versión definitiva para tus columnas exactas:
    codigo, nombre, cantidad, precio, categoria, ubicacion, valor_total
    """
    print("\n=== ANÁLISIS AVANZADO DE INVENTARIO ===")

    # --- Análisis de Stock ---
    print("\n--- Análisis de Stock ---")
    stock_bajo(df, umbral=10)
    stock_excesivo(df, umbral=100)
    promedio_stock_categoria(df)
    productos_sin_stock(df)

    # --- Análisis Económico ---
    print("\n--- Análisis Económico ---")
    valor_total_categoria(df)
    productos_mas_costosos(df, n=5)
    valor_min_max(df)

    # --- Visualizaciones ---
    print("\n--- Visualizaciones ---")
    grafico_distribucion_stock(df)
    grafico_valor_categoria(df)


# ========== FUNCIONES DE ANÁLISIS ==========
def stock_bajo(df, umbral):
    bajo = df[df["cantidad"] < umbral][['codigo', 'nombre', 'cantidad']]
    print(f"\nProductos con menos de {umbral} unidades (stock bajo):")
    print(bajo.to_string(index=False))


def stock_excesivo(df, umbral):
    excesivo = df[df["cantidad"] > umbral][['codigo', 'nombre', 'cantidad']]
    print(f"\nProductos con más de {umbral} unidades (stock excesivo):")
    print(excesivo.to_string(index=False))


def promedio_stock_categoria(df):
    promedio = df.groupby("categoria")["cantidad"].mean().round(1)
    print("\nPromedio de unidades por categoría:")
    print(promedio.to_string())


def productos_sin_stock(df):
    sin_stock = df[df["cantidad"] == 0][['codigo', 'nombre']]
    if not sin_stock.empty:
        print("\n¡ALERTA! Productos agotados:")
        print(sin_stock.to_string(index=False))
    else:
        print("\nNo hay productos agotados en el inventario.")


def valor_total_categoria(df):
    if 'valor_total' not in df.columns:
        df['valor_total'] = df['cantidad'] * df['precio']
    total = df.groupby("categoria")["valor_total"].sum()
    print("\nValor total del inventario por categoría:")
    print(total.to_string())


def productos_mas_costosos(df, n):
    costosos = df.nlargest(n, "precio")[['codigo', 'nombre', 'precio']]
    print(f"\nTop {n} productos más costosos:")
    print(costosos.to_string(index=False))


def valor_min_max(df):
    min_valor = df.loc[df["precio"].idxmin()][['codigo', 'nombre', 'precio']]
    max_valor = df.loc[df["precio"].idxmax()][['codigo', 'nombre', 'precio']]
    print("\nProducto más económico:")
    print(min_valor.to_string())
    print("\nProducto más costoso:")
    print(max_valor.to_string())


# ========== VISUALIZACIONES ==========
BASE_DIR = Path(__file__).resolve().parent.parent  # Ajustar según estructura del proyecto
REPORTS_DIR = BASE_DIR / 'reports'

def grafico_distribucion_stock(df):
    """
    Genera y guarda un histograma de distribución de stock

    Args:
        df (pd.DataFrame): DataFrame con columna 'cantidad' para visualizar

    Returns:
        str: Ruta absoluta donde se guardó el gráfico
    """
    # Configuración del gráfico
    plt.figure(figsize=(10, 6), dpi=100)
    plt.hist(df["cantidad"],
             bins=20,
             color='#1f77b4',
             edgecolor='black',
             alpha=0.7)

    # Estilo profesional
    plt.title("Distribución de Cantidades en Stock", pad=20, fontweight='bold')
    plt.xlabel("Unidades en Stock", labelpad=10)
    plt.ylabel("Frecuencia", labelpad=10)
    plt.grid(axis='y', linestyle=':', alpha=0.4)

    # Ajustar layout automáticamente
    plt.tight_layout()

    # Manejo de rutas y guardado
    REPORTS_DIR.mkdir(exist_ok=True)
    filepath = REPORTS_DIR / 'distribucion_stock.png'

    # Guardado en alta calidad
    plt.savefig(
        filepath,
        dpi=300,
        bbox_inches='tight',
        facecolor='white'
    )

    # Visualización condicional
    if os.getenv('DISPLAY') and plt.isinteractive():
        plt.show()

    plt.close()

    # Retornar ruta para posible uso posterior
    return str(filepath.absolute())


def grafico_valor_categoria(df):
    """
    Genera y guarda un gráfico de barras horizontales del valor por categoría

    Args:
        df (pd.DataFrame): DataFrame con columnas 'cantidad', 'precio' y 'categoria'

    Returns:
        str: Ruta absoluta del archivo guardado
    """
    # Configuración del gráfico
    plt.figure(figsize=(12, 7), dpi=100)
    df["valor_total"] = df["cantidad"] * df["precio"]

    ax = df.groupby("categoria")["valor_total"].sum().sort_values().plot(
        kind='barh',
        color='#2ca02c',
        edgecolor='black',
        alpha=0.7
    )

    # Formateo profesional
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x / 1000:,.0f}K'))
    plt.title("Valor por Categoría (en miles de USD)", pad=20, fontweight='bold')
    plt.xlabel("Valor Total (USD)", labelpad=10)
    plt.grid(axis='x', linestyle=':', alpha=0.4)
    plt.tight_layout()

    # Guardado con rutas absolutas
    filepath = REPORTS_DIR / 'valor_categoria.png'
    plt.savefig(
        filepath,
        dpi=300,
        bbox_inches='tight',
        facecolor='white',
        transparent=False
    )

    # Visualización condicional
    if os.getenv('DISPLAY') and plt.isinteractive():
        plt.show()

    plt.close()

    print(f"\n✅ Gráfico guardado en: {filepath.absolute()}")
    return str(filepath.absolute())