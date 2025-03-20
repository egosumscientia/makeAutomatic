import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Inicializar Faker para datos falsos
fake = Faker()

# Definir número de productos únicos y número de registros
num_products = 1000
num_records = 1000

# Listas de valores aleatorios para algunas columnas
categories = ['Electrónica', 'Ropa', 'Alimentos', 'Hogar', 'Juguetes', 'Deportes', 'Salud', 'Automotriz']
suppliers = ['Proveedor A', 'Proveedor B', 'Proveedor C', 'Proveedor D', 'Proveedor E']
shelf_locations = [f"A-{random.randint(1, 50)}-B{random.randint(1, 20)}" for _ in range(num_records)]

# Crear datos falsos
inventory_data = []
for i in range(num_records):
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
xlsx_path = "inventario.xlsx"
ods_path = "inventario.ods"

df_inventory.to_excel(xlsx_path, index=False)
df_inventory.to_excel(ods_path, index=False, engine="odf")

print(f"Archivos guardados: {xlsx_path}, {ods_path}")
