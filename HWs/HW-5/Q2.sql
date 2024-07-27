create or replace function get_rental_films (_from timestamp, _to timestamp)
	returns table (
		film_title varchar,
		film_release_year int
	) 
	language plpgsql
as $$
begin
	return query 
		SELECT title, release_year::integer
		FROM rental
		INNER JOIN inventory
			ON rental.inventory_id = inventory.inventory_id
		INNER JOIN film
			ON inventory.film_id = film.film_id
		WHERE _from >= rental_date AND _to <= return_date;
end;$$;

SELECT * FROM get_rental_films ('2005-05-24 23:45:30', '2005-05-26 22:04:30');