SELECT 
    CAST(YEAR(DATEADD(YEAR, 20, d.d_date)) AS VARCHAR) + '-' + 
    RIGHT('0' + CAST(MONTH(DATEADD(YEAR, 20, d.d_date)) AS VARCHAR), 2) AS Periodo,
    SUM(s.ss_quantity * s.ss_list_price) AS Total_Ventas
FROM store_sales s
INNER JOIN date_dim d 
    ON s.ss_sold_date_sk = d.d_date_sk
WHERE NOT (
    YEAR(d.d_date) = 2005 
    AND MONTH(d.d_date) = 12
)
GROUP BY 
    YEAR(DATEADD(YEAR, 20, d.d_date)),
    MONTH(DATEADD(YEAR, 20, d.d_date))
ORDER BY 
    MIN(DATEADD(YEAR, 20, d.d_date))