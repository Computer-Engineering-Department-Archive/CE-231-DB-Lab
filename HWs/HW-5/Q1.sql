create or replace function get_number(_number text)
returns text
language plpgsql
as
$$
declare
   _output text;
begin
	SELECT
		CASE
			WHEN SUBSTRING(_number FROM 0 FOR 3) = '09' THEN 'mobile phone number'
			WHEN SUBSTRING(_number FROM 0 FOR 4) = '031' THEN CONCAT('city code=031,', 'last 8 digits=', SUBSTRING(_number FROM 4 FOR 8), ' city=Esfahan')
			WHEN SUBSTRING(_number FROM 0 FOR 4) = '021' THEN CONCAT('city code=021,', 'last 8 digits=', SUBSTRING(_number FROM 4 FOR 8), ' city=Tehran')
			ELSE 'invalid phone number'
		END
   into _output;
   
   return _output;
end;
$$;

-- select get_number('09197270223'); -- Result: mobile phone number
-- select get_number('03144121574'); -- Result: city code=031, last 8 digits=44121574 city=Esfahan
-- select get_number('02144121574'); -- Result: city code=021, last 8 digits=44121574 city=Tehran
-- select get_number('04144121574'); -- Result: invalid phone number