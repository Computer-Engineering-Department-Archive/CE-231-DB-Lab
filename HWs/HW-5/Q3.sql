create or replace function get_rental_films_no_return (_from timestamp)
	returns table (
		customer_first_name varchar,
		customer_last_name varchar
	) 
	language plpgsql
as $$
begin
	return query 
		SELECT customer.first_name, customer.last_name
		FROM rental
		INNER JOIN customer USING(customer_id)
		WHERE _from >= rental_date AND return_date IS NULL;
end;$$;

SELECT * FROM get_rental_films_no_return ('2005-05-24 22:54:33');