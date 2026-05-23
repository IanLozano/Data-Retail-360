# Cargar paquetes
import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, association_rules

conn_str = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-SDA345T\\SQLEXPRESS;'
    'Database=AdventureWorks2019;'
    'Trusted_Connection=yes;'
)

input_query = '''SELECT
     T0.SalesOrderID AS Factura,
     CONVERT(varchar,T1.OrderDate,105) AS Fecha,
     T0.ProductID AS ProductID,
     T2.Name AS Producto,
     T0.OrderQty AS Cantidad,
     T0.UnitPrice AS Precio
  FROM [Sales].[SalesOrderDetail] T0
  JOIN Sales.SalesOrderHeader T1 ON T0.SalesOrderID = T1.SalesOrderID
  JOIN Production.Product T2 ON T0.ProductID = T2.ProductID
'''

data = pd.read_sql(input_query, conn_str)

data.head()

# Explorando las columnas del dataset
data.columns

# quitando espacios extras en el nombre del producto
data['Producto'] = data['Producto'].str.strip()

data.dtypes

# quitando filas sin numero de factura
data.dropna(axis=0, subset=['Factura'], inplace=True)
data['Factura'] = data['Factura'].astype('str')

# Creando el objeto de tipo transacciones
basket = (data
.groupby(['Factura', 'Producto'])['Cantidad']
.sum().unstack().reset_index().fillna(0)
.set_index('Factura'))

basket.head()

# Definición de la función de codificación en caliente para que los datos sean adecuados
# con valores entre 0 y 1
def hot_encode(x):
    if(x <= 0):
        return 0
    if(x >= 1):
        return 1

# Encoding el dataset
basket_encoded = basket.applymap(hot_encode)
basket = basket_encoded

# creando el modelo
frq_items = apriori(basket, min_support=0.03, use_colnames=True)

frq_items.head(10)

# Recopilación de las reglas inferidas en un marco de datos
rules = association_rules(frq_items, metric="lift", min_threshold=0.5)
rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])

print(rules)