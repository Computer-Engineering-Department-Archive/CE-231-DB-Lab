-- create table if not exists tb (
-- 	personel_id int primary key,
-- 	full_name varchar(50),
-- 	username varchar(50) unique
-- );

-- insert into tb values (1, 'keivan ipchi1', 'keivanipchi1');
-- insert into tb values (2, 'keivan ipchi2', 'keivanipchi2');
-- insert into tb values (3, 'keivan ipchi3', 'keivanipchi3');
-- insert into tb values (4, 'keivan ipchi4', 'keivanipchi4');
-- insert into tb values (5, 'keivan ipchi5', 'keivanipchi5');

-- select * from tb;



-- CREATE ROLE testrole
-- SUPERUSER 
-- LOGIN 
-- PASSWORD '1234';

-- SELECT rolname FROM pg_roles;



-- create role group_role
-- SUPERUSER
-- VALID UNTIL '2030-02-03';

-- SELECT rolname FROM pg_roles;



-- create role testrole1 LOGIN PASSWORD '1234';
-- create role testrole2 LOGIN PASSWORD '1234';
-- GRANT group_role to testrole1;
-- GRANT group_role to testrole2;

-- alter role testrole1 INHERIT;
-- alter role testrole1 BYPASSRLS;
-- alter role testrole2 rename to newtstrole2;


-- ALTER TABLE tb ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY test_roles
-- ON tb
-- TO group_role;

drop role newtstrole2;