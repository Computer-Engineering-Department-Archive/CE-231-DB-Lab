(
	(
		select *
		from movies
	)
	INTERSECT
	(
		select *
		from movies
		where imdb < 8
	)
) order by imdb DESC, rotten_tomatoes DESC