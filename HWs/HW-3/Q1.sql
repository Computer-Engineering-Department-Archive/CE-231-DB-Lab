-- Question 1
select genre_id, sum(box_office) box_office, sum(budget) budget, count(budget) count
from movies
group by genre_id;

select genre_id, avg(imdb) imdb, avg(rotten_tomatoes) rotten_tomatoes, count(budget) count
from movies
group by genre_id;

select genre_id, avg(duration) avg_duration, count(budget) count
from movies
group by genre_id;