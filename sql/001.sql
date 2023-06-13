/*markdown
Highlighting 10 wines to recommend
Finding best €/ratings wines, with decent number of ratings but still
favoring less-known, highlight-worthy wines.
*/

SELECT wines.name, ROUND(vintages.price_euros, 2) AS price_euros,  wines.ratings_average, vintages.bottle_volume_ml, wines.ratings_count, wines.url, wines.id
FROM wines
INNER JOIN vintages
ON wines.id = vintages.wine_id
WHERE wines.ratings_count > 200 AND wines.ratings_average > 3.8
ORDER BY (vintages.price_euros/wines.ratings_average/vintages.bottle_volume_ml) ASC
LIMIT 10;

/*markdown
Marketing budget per country  
We are looking for a country with a low users base compared to the population, with a relatively strong wineries base.  
Germany looks like a good candidate for focused marketing.
*/

-- Finding a country to focus marketing on
SELECT *
FROM countries
WHERE wineries_count > 1200
ORDER BY users_count ASC;


/*markdown
Finding the best winery  
The two next cells are different ways to look after a winery worthy of a prize.  
We look for a reliably rated winery, with a good €/rating average, and a satisfying number of vintages.
*/

-- Find the best winery
SELECT wineries.name, AVG(wines.ratings_average)AS winery_avg_rating
FROM wines
INNER JOIN wineries
ON wines.winery_id = wineries.id 
GROUP BY wineries.name
ORDER BY winery_avg_rating DESC
LIMIT 5;

-- Find the best winery, with more refined criterions
SELECT wineries.name, ROUND(AVG(vintages.price_euros),2)  AS winery_avg_price, ROUND(AVG(vintages.ratings_average),2)  AS winery_avg_rating, ROUND(AVG(vintages.ratings_count),2) AS avg_ratings_count, AVG(vintages.price_euros/vintages.ratings_average), COUNT(vintages.name) AS number_of_vintages
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

/*markdown
Find which wines have a combination of 5 specific tastes:
*/

SELECT wines.name, COUNT(keywords.name = "cream")
FROM keywords_wine
INNER JOIN keywords
ON keywords_wine.keyword_id = keywords.id
INNER JOIN wines
ON keywords_wine.wine_id = wines.id
GROUP BY wines.name
HAVING COUNT(keywords.name = "_offee") > 10
    AND COUNT(keywords.name = "_oast") > 10
    AND COUNT(keywords.name = "green apple") > 10
    AND COUNT(keywords.name = "cream") > 10
    AND COUNT(keywords.name = "citrus_fruit") > 10
LIMIT 5;

SELECT keywords.name, COUNT(*)
FROM keywords_wine
INNER JOIN keywords
ON keywords_wine.keyword_id = keywords.id
INNER JOIN wines
ON keywords_wine.wine_id = wines.id
GROUP BY keywords_wine.keyword_id