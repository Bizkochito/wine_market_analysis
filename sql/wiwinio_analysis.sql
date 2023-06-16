/*markdown
Highlighting 10 wines to recommend  
Finding best €/ratings wines, with decent number of ratings but still
favoring less-known, highlight-worthy wines.
*/

SELECT wines.name, ROUND(vintages.price_euros, 2) AS price_euros,  wines.ratings_average, vintages.bottle_volume_ml, wines.ratings_count,  wines.id
FROM wines
INNER JOIN vintages
ON wines.id = vintages.wine_id
WHERE wines.ratings_count > 200 AND wines.ratings_average > 3.8
ORDER BY (vintages.price_euros/wines.ratings_average/vintages.bottle_volume_ml) ASC
LIMIT 10;

/*markdown
Marketing budget per country  
We are looking for a country with a low users base compared to the population, with a relatively strong wineries base.  
Spain and Australia look like good candidates for focused marketing.
*/

-- Finding a country to focus marketing on
SELECT *
FROM countries
WHERE wineries_count > 1200
ORDER BY users_count ASC;

/*markdown
Finding the best winery  
The next cell is a way look after a winery worthy of a prize.  
We select a reliably rated winery, with a good €/rating average, and a satisfying number of vintages.
*/

-- Find the best winery, with more refined criterions
SELECT wineries.name, 
ROUND(AVG(vintages.price_euros),2)  AS winery_avg_price, 
ROUND(AVG(vintages.ratings_average),2)  AS winery_avg_rating, 
ROUND(AVG(vintages.ratings_count),2) AS avg_ratings_count, 
AVG(vintages.price_euros/(vintages.ratings_average)) AS metric, 
COUNT(vintages.name) AS number_of_vintages
FROM vintages
INNER JOIN wines
ON vintages.wine_id = wines.id
INNER JOIN wineries
ON wines.winery_id = wineries.id 
GROUP BY wineries.name
HAVING ROUND(AVG(vintages.price_euros/vintages.ratings_average),2) IS NOT NULL
    AND AVG(vintages.ratings_count) > 50
    AND COUNT(*) > 1
    AND number_of_vintages > 3
    AND winery_avg_rating > 3
ORDER BY metric ASC
LIMIT 8;

/*markdown
It looks like an amazingly sized cluster is centered around the combination of 5 tastes: coffee, toast, cream, citurs and green apple.  
Let us find which wines have a combination of these 5 specific tastes:
*/

SELECT  wines.name, ROUND(vintages.price_euros, 2) AS price_euros,  wines.ratings_average, wines.ratings_count
FROM wines
JOIN keywords_wine
ON wines.id = keywords_wine.wine_id
JOIN vintages
ON wines.id = vintages.wine_id
JOIN keywords
ON keywords_wine.keyword_id =  keywords.id
WHERE keywords_wine.count > 10 
    AND keywords.name IN ('coffee','toast','green apple','cream','citrus')
    AND keywords_wine.keyword_type = 'primary'
GROUP BY wines.name
HAVING COUNT(wines.name)=5;

/*markdown
Next piece of code shows the top grapes used worldwide.
*/

SELECT grapes.name AS Grape, most_used_grapes_per_country.wines_count AS "Total wines"
FROM most_used_grapes_per_country
LEFT JOIN grapes
ON most_used_grapes_per_country.grape_id = grapes.id
GROUP BY grapes.name
ORDER BY most_used_grapes_per_country.wines_count DESC
LIMIT 3;

/*markdown
Let us make a country leaderboard:   
Here we show the average wine rating per country, then average vintage rating per country.   
The vintage rating seems unbalanced in the data, and unreliable to look at.
*/

SELECT countries.name, ROUND(AVG(wines.ratings_average),2) AS average_ratings
FROM wines
INNER JOIN regions
ON wines.region_id = regions.id
INNER JOIN countries
ON regions.country_code = countries.code 
GROUP BY countries.name
ORDER BY average_ratings DESC
LIMIT 5;

SELECT countries.name, ROUND(AVG(vintages.ratings_average),2) AS average_ratings
FROM vintages
INNER JOIN wines
ON vintages.wine_id = wines.id
INNER JOIN regions
ON wines.region_id = regions.id
INNER JOIN countries
ON regions.country_code = countries.code 
GROUP BY countries.name
ORDER BY average_ratings DESC
LIMIT 5;