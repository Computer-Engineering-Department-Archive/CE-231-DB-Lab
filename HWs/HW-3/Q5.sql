select title, release_date, imdb, rotten_tomatoes, box_office, director, duration, budget, genre
from movies
full outer join genres					-- This will add 2 extra rows with many null values
	on genres.id = movies.genre_id		-- The full outer join is redundant helps use all 6 conditions
where
	director is not null				-- This will remove the 2 extra added rows by filtering the NULL values
	and title like '_________%'			-- This will remove 1 row that doesn't satisfy the given condition	
	and genre = any (
		select genre from genres		-- This is redundant, but makes use of 1 condition (:
	)
	and imdb = all (
		select imdb from movies
		where imdb < 7.5				-- This will filter 1 row that doesn't satisfy the given condition
	)
	and exists (
		select *
		from movies
		where
			rotten_tomatoes > 60
	)