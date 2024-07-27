CREATE TABLE IF NOT EXISTS accounts (
	id INT PRIMARY KEY,
	name VARCHAR(50),
	balance DEC (10)
);

BEGIN;
	INSERT INTO accounts (id, name, balance) VALUES (1, 'Keivan1', 30);
	SAVEPOINT one;
	
	INSERT INTO accounts (id, name, balance) VALUES (2, 'Keivan2', 30);
	ROLLBACK TO SAVEPOINT one;
	
	INSERT INTO accounts (id, name, balance) VALUES (3, 'Keivan3', 30);
	SAVEPOINT three;
	
	INSERT INTO accounts (id, name, balance) VALUES (4, 'Keivan4', 30);
	ROLLBACK TO SAVEPOINT three;
	
	INSERT INTO accounts (id, name, balance) VALUES (5, 'Keivan5', 30);
	SAVEPOINT five;
COMMIT;