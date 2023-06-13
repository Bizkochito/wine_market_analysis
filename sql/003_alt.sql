-- Find the best winery
SELECT wineries.name, ROUND(AVG(vintages.price_euros),2)  AS winery_avg_price, ROUND(AVG(vintages.ratings_average),2)  AS winery_avg_rating, ROUND(AVG(vintages.ratings_count),2) AS avg_ratings_count, AVG(vintages.price_euros/vintages.ratings_average), COUNT(*) AS number_of_vintages
FROM vintages
INNER JOIN wines
ON vintages.wine_id = wines.id
INNER JOIN wineries
ON wines.winery_id = wineries.id 
GROUP BY wineries.name
HAVING ROUND(AVG(vintages.price_euros/vintages.ratings_average),2) IS NOT NULL
    AND AVG(vintages.ratings_count) > 50
    AND COUNT(*) > 1
ORDER BY AVG(vintages.price_euros/vintages.ratings_average) ASC
LIMIT 8;