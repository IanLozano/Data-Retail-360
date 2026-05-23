WITH ventas_por_cliente AS (
    SELECT
        s.ss_customer_sk AS id_cliente,
        COUNT(DISTINCT s.ss_ticket_number) AS total_pedidos,
        COUNT(s.ss_item_sk) AS total_items,
        SUM(s.ss_net_paid) AS total_dinero
    FROM dbo.store_sales s
    GROUP BY s.ss_customer_sk
),
devoluciones_por_cliente AS (
    SELECT
        r.sr_customer_sk AS id_cliente,
        COUNT(DISTINCT r.sr_ticket_number) AS pedidos_devueltos,
        COUNT(r.sr_item_sk) AS items_devueltos,
        SUM(r.sr_return_amt) AS dinero_devuelto
    FROM dbo.store_returns r
    GROUP BY r.sr_customer_sk
),
base AS (
    SELECT
        v.id_cliente,
        v.total_pedidos,
        v.total_items,
        v.total_dinero,
        COALESCE(d.pedidos_devueltos, 0) AS pedidos_devueltos,
        COALESCE(d.items_devueltos, 0) AS items_devueltos,
        COALESCE(d.dinero_devuelto, 0) AS dinero_devuelto
    FROM ventas_por_cliente v
    LEFT JOIN devoluciones_por_cliente d
        ON v.id_cliente = d.id_cliente
),
percentiles AS (
    SELECT DISTINCT
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_dinero) OVER () AS p75_gasto,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY total_dinero) OVER () AS p25_gasto,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_pedidos) OVER () AS p75_frecuencia
    FROM base
)
SELECT
    b.id_cliente AS cliente,

    c.c_first_name AS nombre,
    c.c_last_name AS apellido,
    CONCAT(c.c_first_name, ' ', c.c_last_name) AS nombre_cliente,
    c.c_email_address AS correo_electronico,

    a.ca_street_number AS numero_direccion,
    a.ca_street_name AS calle,
    a.ca_street_type AS tipo_calle,
    a.ca_suite_number AS complemento_direccion,
    a.ca_city AS ciudad,
    a.ca_county AS condado,
    a.ca_state AS estado,
    a.ca_zip AS codigo_postal,
    a.ca_country AS pais_direccion,
    a.ca_location_type AS tipo_ubicacion,

    b.total_pedidos AS frecuencia_compra,
    b.total_items,
    b.total_dinero AS gasto_total,

    ROUND(
        CASE
            WHEN b.total_pedidos = 0 THEN 0
            ELSE b.total_dinero * 1.0 / b.total_pedidos
        END
    , 7) AS ticket_promedio,

    ROUND(
        CASE
            WHEN b.total_pedidos = 0 THEN 0
            ELSE b.pedidos_devueltos * 1.0 / b.total_pedidos
        END
    , 7) AS ratio_pedidos,

    ROUND(
        CASE
            WHEN b.total_items = 0 THEN 0
            ELSE b.items_devueltos * 1.0 / b.total_items
        END
    , 7) AS ratio_items,

    ROUND(
        CASE
            WHEN b.total_dinero = 0 THEN 0
            ELSE b.dinero_devuelto * 1.0 / b.total_dinero
        END
    , 7) AS ratio_dinero,

    b.pedidos_devueltos AS frecuencia_devoluciones,

    CASE
        WHEN 
            CASE
                WHEN b.total_dinero = 0 THEN 0
                ELSE b.dinero_devuelto * 1.0 / b.total_dinero
            END > 0.30
            THEN 'Riesgoso'

        WHEN b.total_dinero >= p.p75_gasto
             AND b.total_pedidos >= p.p75_frecuencia
            THEN 'Alto Valor'

        WHEN b.total_dinero <= p.p25_gasto
            THEN 'Bajo Valor'

        ELSE 'Medio'
    END AS riesgo_cliente

FROM base b
CROSS JOIN percentiles p
LEFT JOIN dbo.customer c
    ON b.id_cliente = c.c_customer_sk
LEFT JOIN dbo.customer_address a
    ON c.c_current_addr_sk = a.ca_address_sk;