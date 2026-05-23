SELECT
    T0.c_customer_sk AS id_cliente,
    CONCAT_WS(' ', T0.c_first_name, T0.c_last_name) AS nombre_cliente,
    T0.c_birth_day AS dia_nacimiento,
    T0.c_birth_month AS mes_nacimiento,
    T0.c_birth_year + 20 AS anio_nacimiento,
    T0.c_birth_country AS pais_nacimiento,
    T0.c_last_review_date AS fecha_revision
FROM dbo.customer T0;