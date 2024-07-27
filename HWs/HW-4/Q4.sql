-- 4
SELECT
	film.title,
	category.name AS category,
	film.length,
	ROW_NUMBER() OVER (
		PARTITION BY category
		ORDER BY length
	) AS rank_in_category
FROM
	film_category
INNER JOIN film USING(film_id)
INNER JOIN category USING(category_id)