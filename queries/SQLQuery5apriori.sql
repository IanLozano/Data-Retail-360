SELECT 
    det.SalesOrderID AS NumeroFactura,
    FORMAT(cab.OrderDate, 'dd-MM-yyyy') AS FechaPedido,
    det.ProductID AS IdProducto,
    prod.Name AS NombreProducto,
    det.OrderQty AS CantidadVendida,
    det.UnitPrice AS PrecioUnitario
FROM sales.SalesOrderDetail AS det
INNER JOIN sales.SalesOrderHeader AS cab 
    ON det.SalesOrderID = cab.SalesOrderID
INNER JOIN Production.Product AS prod 
    ON det.ProductID = prod.ProductID;