-- Finding a country to focus marketing on
SELECT *
FROM countries
WHERE wineries_count > 1200
ORDER BY users_count ASC;