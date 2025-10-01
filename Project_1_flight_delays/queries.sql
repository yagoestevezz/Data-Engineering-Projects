-- Wich airlines has the most delayed flights?
SELECT
    t2.airline_code,
    COUNT(*) AS count_of_delayed_flights
FROM
    fact_delay as t1
inner join 
	dim_flight_info as t2
on t1.flight_id = t2.flight_id	
GROUP BY
    t2.airline_code
ORDER BY
    count_of_delayed_flights DESC;
    
-- Which origin airpports has the most delayed flights?
SELECT
    origin_airport_id,  
    COUNT(*) AS count_of_delayed_flights
FROM
    fact_delay
GROUP BY
    origin_airport_id 
ORDER BY
    count_of_delayed_flights DESC;

-- How do holidays affect the delay?    
SELECT
    MONTHNAME(t2.full_date) AS month_name,
    DAYNAME(t2.full_date) AS day_of_week,
    CASE
        WHEN t2.is_holiday = TRUE THEN 'YES'
        ELSE 'NO '
    END AS is_holiday_status,
    AVG(t1.departure_delay) AS avg_delay_minutes,
    COUNT(*) AS total_delayed_flights
FROM
    fact_delay AS t1
JOIN
    dim_date AS t2 ON t1.date_id = t2.date_id
GROUP BY
    month_name, day_of_week, is_holiday_status
ORDER BY
    avg_delay_minutes DESC;

-- Which hours have the most delays?
SELECT
    T.hour_of_day, 
    T.period_of_day,
    COUNT(FD.delay_id) AS total_dealayed_flights
FROM
    fact_delay FD
JOIN
    dim_time T ON FD.hour_scheduled_id = T.time_id
GROUP BY
    T.hour_of_day, T.period_of_day
ORDER BY
    total_dealayed_flights DESC
LIMIT 5;

-- Which months have the most delays?
SELECT
    MONTH(D.full_date) AS month_number,
    MONTHNAME(D.full_date) AS month_name,
    COUNT(FD.delay_id) AS total_delayed_flights
FROM
    fact_delay FD
JOIN
    dim_date D ON FD.date_id = D.date_id
GROUP BY
    month_number, month_name
ORDER BY
    total_delayed_flights DESC
LIMIT 12;
