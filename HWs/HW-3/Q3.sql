with cte_movie as (
	select title, release_date, imdb, rotten_tomatoes, box_office, director, duration, budget, genre
	from movies
	natural join genres
)
select title, director, genre
from cte_movie