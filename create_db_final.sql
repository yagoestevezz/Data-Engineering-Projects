create database flight_delays;
use flight_delays;

create table dim_date(
	date_id int  primary key,
    full_date date,
    is_holiday boolean
	);
CREATE TABLE dim_time (
  time_id varchar(5) PRIMARY KEY,
  full_time TIME NOT NULL,
  hour_of_day INT NOT NULL,
  minute_of_hour INT NOT NULL,
  period_of_day VARCHAR(10) NOT NULL
);

create table dim_flight_info(
flight_id varchar(20) PRIMARY KEY,
airline_code char(2),
airline_name varchar(35),
flight_number char(4),
tail_number varchar (10)
);
create table dim_airport(
airport_id varchar(5) PRIMARY KEY,
airport_name varchar(100),
state varchar(4),
city varchar(50)
);
create table fact_delay(
delay_id int auto_increment primary key,
flight_id varchar(20),
date_id int, 
hour_departure_id varchar(5),
hour_scheduled_id varchar(5),
origin_airport_id varchar(5),
destination_airport_id varchar(5),

departure_delay int,
	CONSTRAINT fk_delay_date
        FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id),
	CONSTRAINT fk_delay_time_dep
		FOREIGN KEY (hour_departure_id)
        REFERENCES dim_time(time_id),
	CONSTRAINT fk_delay_time_schedule
		FOREIGN KEY (hour_scheduled_id)
        REFERENCES dim_time(time_id),	
	CONSTRAINT fk_delay_flight
		FOREIGN KEY (flight_id)
        REFERENCES dim_flight_info(flight_id),
	CONSTRAINT fk_delay_airport_origin
		FOREIGN KEY (origin_airport_id)
        REFERENCES dim_airport(airport_id),
	CONSTRAINT fk_delay_airport_destination
		FOREIGN KEY (destination_airport_id)
        REFERENCES dim_airport(airport_id)
);
show databases;
select * 
from fact_delay
limit 100;

--   drop database flight_delays;
 
 