-- SELECT * FROM movies;

-- Q1
-- ALTER TABLE movies
-- ADD COLUMN budget money,
-- ADD COLUMN genre_id integer,
-- ADD FOREIGN KEY (genre_id) REFERENCES genres(id);

-- Q3
-- INSERT INTO genres (id, genre)
-- 	VALUES(0, 'romance');

-- 	VALUES (0, 'The Fault in Our Stars','June 6, 2014', 7.6, 81, '$307000000', 'Josh Boone', 126, '$8500000', 0);

-- UPDATE movies
-- SET "IMDB" = 7.7
-- WHERE movies.id = 0;

-- -- Select
-- SELECT * FROM movies;

-- Q4
-- CREATE VIEW detailed_movies AS
-- SELECT M.id, M.title, G.genre
-- FROM movies as M
-- 	JOIN genres AS G ON G.id = M.genre_id;

-- SELECT * FROM detailed_movies