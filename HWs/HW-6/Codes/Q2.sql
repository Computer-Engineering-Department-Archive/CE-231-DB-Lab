-- Worker 1
BEGIN;
	SELECT balance
	FROM   accounts
	WHERE  id = 1
	FOR    UPDATE;
	
	UPDATE accounts
	SET    balance = 100
	WHERE  id = 2;

-- Worker 2
BEGIN;
	SELECT balance 
	FROM   accounts
	WHERE  id = 2
	FOR    UPDATE;
	
	UPDATE accounts
	SET    balance = 100
	WHERE  id = 1;