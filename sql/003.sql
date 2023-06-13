-- Find the best winery
SELECT wineries.name, AVG(wines.ratings_average)AS winery_avg_rating
FROM wines
INNER JOIN wineries
ON wines.winery_id = wineries.id 
GROUP BY wineries.name
ORDER BY winery_avg_rating DESC
LIMIT 5;