-- Create table
create table log (
	id SERIAL primary key,
	customer_id int,
	delays int,
	
	foreign key (customer_id) references customer(customer_id)
);

-- Create function
CREATE OR REPLACE FUNCTION rental_update()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
	IF EXTRACT(day FROM NEW.return_date - NEW.rental_date) > (
		SELECT rental_duration
		FROM film
		INNER JOIN inventory USING (film_id)
		INNER JOIN rental USING (inventory_id)
		WHERE rental.rental_id = NEW.rental_id
		LIMIT 1
	) THEN
		
		INSERT INTO log (customer_id, delays)
		VALUES (NEW.customer_id, 123);
	END IF;

	RETURN NEW;
END;
$$;

-- Add function to trigger
CREATE TRIGGER last_name_changes
BEFORE UPDATE
	ON rental
FOR EACH ROW
EXECUTE PROCEDURE rental_update();

CREATE TRIGGER last_name_changes
BEFORE INSERT
	ON rental
FOR EACH ROW
EXECUTE PROCEDURE rental_update();

-- Test trigger
UPDATE rental
SET staff_id = 1
WHERE rental_id = 4;


-- SELECT rental_id, title, EXTRACT(day FROM return_date - rental_date) - rental_duration
-- FROM film
-- INNER JOIN inventory USING (film_id)
-- INNER JOIN rental USING (inventory_id)