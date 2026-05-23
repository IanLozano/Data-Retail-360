import pyodbc
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# SOLO la primera vez (fuera de Power BI si jode)
nltk.download('vader_lexicon')

# 👇 TU conexión (bien escrita)
conexion = pyodbc.connect(
    r"Driver={SQL Server};"
    r"Server=DESKTOP-SDA345T\SQLEXPRESS;"
    r"Database=tpcxbb_1gb;"
    r"Trusted_Connection=yes;"
)

consulta = """
SELECT
    r.pr_review_date AS Fecha_Review,
    r.pr_item_sk AS ID_Producto,
    r.pr_review_rating AS Rating,
    r.pr_review_content AS Texto_Review,
    r.pr_user_sk AS ID_Usuario,
    i.i_category AS Categoria,
    i.i_product_name AS Nombre_Producto,
    i.i_item_desc AS Descripcion,
    i.i_size AS Tamano
FROM product_reviews r
INNER JOIN item i
    ON r.pr_item_sk = i.i_item_sk
"""

df = pd.read_sql(consulta, conexion)

analizador = SentimentIntensityAnalyzer()

df["score_sentimiento"] = df["Texto_Review"].fillna("").apply(
    lambda x: round(analizador.polarity_scores(x)["compound"], 2)
)

print(df.head())