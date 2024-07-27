select title, release_date, imdb, genre, duration
from movies
inner join genres
	on genres.id = movies.genre_id;

select title, release_date, imdb, genre, duration
from movies
right outer join genres
	on genres.id = movies.genre_id;