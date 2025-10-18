create database project2_f1;
use project2_f1;

create table dim_driver(
-- driver_id int  primary key,
driver_id varchar(20) primary key,
`name` varchar(20),
surname varchar(30),
nationality varchar(20),
date_of_birth date
);

create table dim_constructor(
-- constructor_id int primary key,
constructor_id varchar(25) primary key ,
`name` varchar(25),
nationality varchar(20)
);

create table dim_circuit(
-- circuit_id int primary key,
circuit_id varchar(20) primary key,
`name` varchar(40),
location varchar(25),
country varchar(15),
latitude decimal(10,7),
longitude decimal(10,7),
altitude int
);

create table dim_race(
race_id varchar(10) primary key,
`date` date,
round int
);

create table fact_qualy(
qualy_id int auto_increment primary key,
driver_id varchar(20),
constructor_id  varchar(25),
circuit_id varchar(20),
race_id varchar(10),
q1 int,
q2 int,
q3 int,
	CONSTRAINT fk_qualy_driver
        FOREIGN KEY (driver_id)
        REFERENCES dim_driver(driver_id),

	CONSTRAINT fk_qualy_constructor
        FOREIGN KEY (constructor_id)
        REFERENCES dim_constructor(constructor_id),

	CONSTRAINT fk_qualy_circuit
        FOREIGN KEY (circuit_id)
        REFERENCES dim_circuit(circuit_id),

	CONSTRAINT fk_qualy_race
        FOREIGN KEY (race_id)
        REFERENCES dim_race(race_id)
);

-- drop database project2_f1;
