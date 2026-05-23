SELECT
    r.pr_review_date AS Fecha_Review,
    r.pr_item_sk AS ID_Producto,
    r.pr_review_rating AS Rating,
    r.pr_review_content AS Texto_Review,
    r.pr_user_sk AS ID_Usuario,

    i.i_category AS Categoria_Producto,
    i.i_product_name AS Nombre_Producto,
    i.i_item_desc AS Detalle_Producto,
    i.i_size AS Tamano

FROM product_reviews r
INNER JOIN item i
    ON r.pr_item_sk = i.i_item_sk;