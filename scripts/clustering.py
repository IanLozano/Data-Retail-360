import pyodbc
import matplotlib
matplotlib.use('TkAgg')  # asegura que se abra la ventana del gráfico
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import distance as distancia
from sklearn import cluster as agrupamiento

# =========================
# CONEXIÓN
# =========================
conexion = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-SDA345T\\SQLEXPRESS;'
    'Database=tpcxbb_1gb;'
    'Trusted_Connection=yes;'
)

# =========================
# QUERY
# =========================
consulta_sql = '''
SELECT
    base.id_cliente AS cliente,
    ROUND(
        CASE
            WHEN base.total_pedidos = 0 THEN 0
            ELSE ISNULL(dev.pedidos_devueltos, 0) * 1.0 / base.total_pedidos
        END
    , 7) AS ratio_pedidos,
    ROUND(
        CASE
            WHEN base.total_items = 0 THEN 0
            ELSE ISNULL(dev.items_devueltos, 0) * 1.0 / base.total_items
        END
    , 7) AS ratio_items,
    ROUND(
        CASE
            WHEN base.total_dinero = 0 THEN 0
            ELSE ISNULL(dev.dinero_devuelto, 0) * 1.0 / base.total_dinero
        END
    , 7) AS ratio_dinero,
    ISNULL(dev.pedidos_devueltos, 0) AS frecuencia_devoluciones
FROM
(
    SELECT
        ss_customer_sk AS id_cliente,
        COUNT(DISTINCT ss_ticket_number) AS total_pedidos,
        COUNT(ss_item_sk) AS total_items,
        SUM(ss_net_paid) AS total_dinero
    FROM store_sales
    GROUP BY ss_customer_sk
) base
LEFT JOIN
(
    SELECT
        sr_customer_sk AS id_cliente,
        COUNT(DISTINCT sr_ticket_number) AS pedidos_devueltos,
        COUNT(sr_item_sk) AS items_devueltos,
        SUM(sr_return_amt) AS dinero_devuelto
    FROM store_returns
    GROUP BY sr_customer_sk
) dev
    ON base.id_cliente = dev.id_cliente
'''

# =========================
# CARGA DE DATOS
# =========================
datos_clientes = pd.read_sql(consulta_sql, conexion)

print("Primeras filas:")
print(datos_clientes.head(5))

# =========================
# MÉTODO DEL CODO
# =========================
datos_modelo = datos_clientes[[
    "ratio_pedidos",
    "ratio_items",
    "ratio_dinero",
    "frecuencia_devoluciones"
]]

valores_k = range(1, 20)

modelos = [
    agrupamiento.KMeans(n_clusters=k, random_state=111, n_init=10).fit(datos_modelo)
    for k in valores_k
]

centros = [m.cluster_centers_ for m in modelos]

distancias = [
    distancia.cdist(datos_modelo, c, 'euclidean')
    for c in centros
]

dist_min = [np.min(d, axis=1) for d in distancias]

promedio_interno = [
    np.sum(d) / datos_modelo.shape[0]
    for d in dist_min
]

# =========================
# GRÁFICO (YA FUNCIONA)
# =========================
plt.figure()
plt.plot(list(valores_k), promedio_interno, 'b*-')
plt.grid(True)
plt.xlabel('Numero de clusters')
plt.ylabel('Promedio distancia interna')
plt.title('Metodo del codo KMeans')
plt.savefig("metodo_codo.png")  # guarda imagen
plt.show()  # muestra ventana

# =========================
# KMEANS FINAL
# =========================
cantidad_clusters = 4

modelo_final = agrupamiento.KMeans(
    n_clusters=cantidad_clusters,
    random_state=111,
    n_init=10
)

modelo_final.fit(datos_modelo)

datos_clientes["cluster"] = modelo_final.labels_

# =========================
# RESULTADOS
# =========================
for i in range(cantidad_clusters):
    grupo = datos_clientes[datos_clientes["cluster"] == i]
    print(f'Cluster {i} (n={len(grupo)}):')
    print('-' * 20)

print(
    datos_clientes
    .groupby("cluster")[[
        "ratio_pedidos",
        "ratio_items",
        "ratio_dinero",
        "frecuencia_devoluciones"
    ]]
    .mean()
)

# =========================
# CERRAR CONEXIÓN
# =========================
conexion.close()