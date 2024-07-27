-- 2
SELECT
	extract(year from payment_date) AS year,		-- Year
	extract(month from payment_date) AS month,		-- Month
	extract(day from payment_date) AS day,			-- Day
	SUM(amount)
FROM
	payment
GROUP BY
	ROLLUP(year, month, day)
ORDER BY
	year, month, day