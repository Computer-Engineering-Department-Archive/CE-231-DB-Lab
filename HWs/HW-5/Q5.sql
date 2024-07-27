create or replace procedure increase_rental_duration(
   	amount integer,
	idk int
)
language plpgsql    
as $$
begin
    update film 
    set rental_duration = rental_duration - amount;

    commit;
end;$$;

call increase_rental_duration(1, 0);

select *
from film