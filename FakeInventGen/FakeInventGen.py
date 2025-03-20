import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import numpy as np

# Inicializar Faker para datos falsos
fake = Faker()

# Definir número de productos únicos y número de registros
num_products = 1000
num_records = 1000

# Listas de valores aleatorios para algunas columnas
categories = ['Electrónica', 'Ropa', 'Alimentos', 'Hogar', 'Juguetes', 'Deportes', 'Salud', 'Automotriz']
suppliers = ['Proveedor A', 'Proveedor B', 'Proveedor C', 'Proveedor D', 'Proveedor E']
shelf_locations = [f"A-{random.randint(1, 50)}-B{random.randint(1, 20)}" for _ in range(num_records)]

# Probabilidad de insertar filas defectuosas
defective_prob = 0.1  # 10% de las filas serán defectuosas

def generate_corrupt_row():
    """Genera una fila con datos corruptos o mal formateados."""
    corruption_type = random.choice(['null', 'empty', 'wrong_format', 'random_chars'])
    if corruption_type == 'null':
        return [None] * 8  # Toda la fila es nula
    elif corruption_type == 'empty':
        return [''] * 8  # Toda la fila es vacía
    elif corruption_type == 'wrong_format':
        return [
            random.randint(1000, 9999),  # Número en lugar de ID
            fake.sentence(),  # Frase en lugar de nombre de producto
            random.randint(0, 9999),  # Número en lugar de categoría
            '???',  # Caracteres no válidos en cantidad
            'PrecioX',  # Cadena en vez de precio
            12345,  # Número en vez de proveedor
            'FechaIncorrecta',  # Fecha incorrecta
            'Ubicación' + str(random.randint(100, 999))  # Ubicación mal formada
        ]
    elif corruption_type == 'random_chars':
        return [
            ''.join(random.choices('!@#$%^&*()', k=5)),  # Caracteres extraños
            ''.join(random.choices('1234567890', k=8)),  # Solo números
            ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10)),
            '',
            'NaN',
            None,
            '????',
            'Random' + str(random.randint(1, 999))
        ]

# Crear datos falsos con filas defectuosas
inventory_data = []
for i in range(num_records):
    if random.random() < defective_prob:
        inventory_data.append(generate_corrupt_row())
    else:
        product_id = f"P-{i + 1:04d}"
        product_name = fake.word().capitalize() + " " + fake.word().capitalize()
        category = random.choice(categories)
        stock_quantity = random.randint(1, 500)
        unit_price = round(random.uniform(1, 500), 2)
        supplier = random.choice(suppliers)
        entry_date = datetime.today() - timedelta(days=random.randint(0, 730))
        warehouse_location = random.choice(shelf_locations)

        inventory_data.append([
            product_id, product_name, category, stock_quantity, unit_price,
            supplier, entry_date.strftime("%Y-%m-%d"), warehouse_location
        ])

# Crear DataFrame
df_inventory = pd.DataFrame(inventory_data, columns=[
    'ID Producto', 'Nombre Producto', 'Categoría', 'Cantidad en Stock',
    'Precio Unitario', 'Proveedor', 'Fecha de Ingreso', 'Ubicación en Almacén'
])

# Guardar en formatos .xlsx y .ods
xlsx_path = "inventario_corrupto.xlsx"
ods_path = "inventario_corrupto.ods"

df_inventory.to_excel(xlsx_path, index=False)
df_inventory.to_excel(ods_path, index=False, engine="odf")

print(f"Archivos guardados con datos corruptos: {xlsx_path}, {ods_path}")
