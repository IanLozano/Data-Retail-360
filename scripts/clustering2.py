import pyodbc
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import distance as distancia
from sklearn import cluster as agrupamiento
from sklearn.preprocessing import StandardScaler

conexion = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-SDA345T\\SQLEXPRESS;'
    'Database=tpcxbb_1gb;'
    'Trusted_Connection=yes;'
)

consulta_sql = '''
SELECT
    ventas.id_cliente AS id_cliente,
    cli.nombre_cliente,
    cli.edad,
    cli.pais_nacimiento,
    ventas.total_pedidos AS frecuencia_compra,
    ventas.total_dinero AS gasto_total,
    ROUND(
        CASE
            WHEN ventas.total_pedidos = 0 THEN 0
            ELSE ventas.total_dinero * 1.0 / ventas.total_pedidos
        END
    , 7) AS ticket_promedio,
    ROUND(
        CASE
            WHEN ventas.total_pedidos = 0 THEN 0
            ELSE ISNULL(dev.pedidos_devueltos, 0) * 1.0 / ventas.total_pedidos
        END
    , 7) AS ratio_pedidos,
    ROUND(
        CASE
            WHEN ventas.total_items = 0 THEN 0
            ELSE ISNULL(dev.items_devueltos, 0) * 1.0 / ventas.total_items
        END
    , 7) AS ratio_items,
    ROUND(
        CASE
            WHEN ventas.total_dinero = 0 THEN 0
            ELSE ISNULL(dev.dinero_devuelto, 0) * 1.0 / ventas.total_dinero
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
    FROM dbo.store_sales
    GROUP BY ss_customer_sk
) ventas
LEFT JOIN
(
    SELECT
        sr_customer_sk AS id_cliente,
        COUNT(DISTINCT sr_ticket_number) AS pedidos_devueltos,
        COUNT(sr_item_sk) AS items_devueltos,
        SUM(sr_return_amt) AS dinero_devuelto
    FROM dbo.store_returns
    GROUP BY sr_customer_sk
) dev
    ON ventas.id_cliente = dev.id_cliente
LEFT JOIN
(
    SELECT
        base.id_cliente,
        base.nombre_cliente,
        base.pais_nacimiento,
        CASE
            WHEN base.fecha_nacimiento IS NOT NULL
            THEN DATEDIFF(YEAR, base.fecha_nacimiento, GETDATE())
                 - CASE
                     WHEN DATEADD(
                         YEAR,
                         DATEDIFF(YEAR, base.fecha_nacimiento, GETDATE()),
                         base.fecha_nacimiento
                     ) > CAST(GETDATE() AS date)
                     THEN 1
                     ELSE 0
                   END
            ELSE NULL
        END AS edad
    FROM
    (
        SELECT
            c_customer_sk AS id_cliente,
            CONCAT_WS(' ', c_first_name, c_last_name) AS nombre_cliente,
            c_birth_country AS pais_nacimiento,
            TRY_CONVERT(
                date,
                CONCAT(
                    c_birth_year + 20, '-',
                    RIGHT('00' + CAST(c_birth_month AS varchar(2)), 2), '-',
                    RIGHT('00' + CAST(c_birth_day AS varchar(2)), 2)
                )
            ) AS fecha_nacimiento
        FROM dbo.customer
    ) base
) cli
    ON ventas.id_cliente = cli.id_cliente
'''

datos_clientes = pd.read_sql(consulta_sql, conexion)

print("Primeras filas:")
print(datos_clientes.head(5))

columnas_modelo = [
    "edad",
    "frecuencia_compra",
    "gasto_total",
    "ticket_promedio",
    "ratio_pedidos",
    "ratio_items",
    "ratio_dinero",
    "frecuencia_devoluciones"
]

datos_modelo = datos_clientes[columnas_modelo].copy()
datos_modelo = datos_modelo.dropna()

print("\nCantidad de registros para clustering:", len(datos_modelo))

escalador = StandardScaler()
datos_escalados = escalador.fit_transform(datos_modelo)

valores_k = range(1, 20)

modelos = [
    agrupamiento.KMeans(n_clusters=k, random_state=111, n_init=10).fit(datos_escalados)
    for k in valores_k
]

centros = [modelo.cluster_centers_ for modelo in modelos]

distancias = [
    distancia.cdist(datos_escalados, centro, 'euclidean')
    for centro in centros
]

distancias_minimas = [np.min(d, axis=1) for d in distancias]

promedio_interno = [
    np.sum(d) / datos_escalados.shape[0]
    for d in distancias_minimas
]

plt.figure()
plt.plot(list(valores_k), promedio_interno, 'b*-')
plt.grid(True)
plt.xlabel('Numero de clusters')
plt.ylabel('Promedio distancia interna')
plt.title('Metodo del codo KMeans')
plt.savefig("metodo_codo_mejorado.png")
plt.show()

cantidad_clusters = 4

modelo_final = agrupamiento.KMeans(
    n_clusters=cantidad_clusters,
    random_state=111,
    n_init=10
)

modelo_final.fit(datos_escalados)

datos_resultado = datos_clientes.loc[datos_modelo.index].copy()
datos_resultado["cluster"] = modelo_final.labels_

for i in range(cantidad_clusters):
    grupo = datos_resultado[datos_resultado["cluster"] == i]
    print(f'\nCluster {i} (n={len(grupo)}):')
    print('-' * 30)

print("\nPromedios por cluster:")
print(
    datos_resultado
    .groupby("cluster")[[
        "edad",
        "frecuencia_compra",
        "gasto_total",
        "ticket_promedio",
        "ratio_pedidos",
        "ratio_items",
        "ratio_dinero",
        "frecuencia_devoluciones"
    ]]
    .mean()
)

conexion.close()