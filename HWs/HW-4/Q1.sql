SELECT *
FROM CROSSTAB('
	WITH rents AS(
		SELECT *
		FROM rental
		INNER JOIN inventory USING (inventory_id)
	), films AS (		-- Connect films, film_category & category
		SELECT *
		FROM film
		INNER JOIN film_category USING (film_id)
	)
	SELECT
		store_id AS store,
		category_id AS category,
		COUNT(*)
	FROM rents
	INNER JOIN films USING (film_id)
	GROUP BY
		store_id, category
	ORDER BY
		1, 2'
	, 'select m from generate_series(1, 16) m') AS (
	store int,
	"Action" int,
	"Animation" int,
	"Children" int,
	"Classics" int,
	"Comedy" int,
	"Documentary" int,
	"Drama" int,
	"Family" int,
	"Foreign" int,
	"Games" int,
	"Horror" int,
	"Music" int,
	"New" int,
	"Sci-Fi" int,
	"Sports" int,
	"Travel" int
);