import warnings
warnings.filterwarnings("ignore")

import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima, ADFTest
from sklearn.metrics import r2_score


conexion = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-SDA345T\\SQLEXPRESS;"
    "DATABASE=tpcxbb_1gb;"
    "Trusted_Connection=yes;"
)

consulta_sql = """
SELECT 
    CAST(YEAR(d.d_date) AS VARCHAR) + '-' + 
    RIGHT('0' + CAST(MONTH(d.d_date) AS VARCHAR), 2) AS Periodo,
    SUM(s.ss_quantity * s.ss_list_price) AS Total_Ventas
FROM store_sales s
INNER JOIN date_dim d
    ON s.ss_sold_date_sk = d.d_date_sk
WHERE NOT (
    YEAR(d.d_date) = 2005
    AND MONTH(d.d_date) = 12
)
GROUP BY 
    YEAR(d.d_date),
    MONTH(d.d_date)
ORDER BY 
    MIN(d.d_date)
"""

ventas_mensuales = pd.read_sql(consulta_sql, conexion)

ventas_mensuales.head()
ventas_mensuales.tail()
ventas_mensuales.dtypes

ventas_mensuales["Periodo"] = pd.to_datetime(ventas_mensuales["Periodo"])
ventas_mensuales.dtypes

serie_ventas = ventas_mensuales.set_index("Periodo")
serie_ventas.head()

serie_ventas.plot()

prueba_adf = ADFTest(alpha=0.05)
prueba_adf.should_diff(serie_ventas)

datos_entrenamiento = serie_ventas.iloc[:85]
datos_prueba = serie_ventas.iloc[-20:]

datos_entrenamiento.tail()
datos_prueba.head()

plt.plot(datos_entrenamiento)
plt.plot(datos_prueba)

modelo_sarima = auto_arima(
    datos_entrenamiento,
    start_p=0,
    d=1,
    start_q=0,
    max_p=5,
    max_d=5,
    max_q=5,
    start_P=0,
    D=1,
    start_Q=0,
    max_P=5,
    max_D=5,
    max_Q=5,
    m=12,
    seasonal=True,
    error_action='warn',
    trace=True,
    supress_warnings=True,
    stepwise=True,
    random_state=20,
    n_fits=50
)

modelo_sarima.summary()

pronostico = modelo_sarima.predict(n_periods=20)
df_pronostico = pd.DataFrame(pronostico, index=datos_prueba.index, columns=["predicted_sales"])

df_pronostico

plt.figure(figsize=(8, 5))
plt.plot(datos_entrenamiento, label="Training")
plt.plot(datos_prueba, label="Test")
plt.plot(df_pronostico, label="Predicted")
plt.legend(loc="best")
plt.show()

datos_prueba["predicted_sales"] = df_pronostico["predicted_sales"]
r2_score(datos_prueba["Total_Ventas"], datos_prueba["predicted_sales"])

resultado_completo = pd.concat([serie_ventas, df_pronostico], axis=0)