create table world_records (
id integer primary key,
distance varchar(20),
course varchar(3),
gender varchar(1),
fullname varchar(100),
nationality varchar(3),
swimtime varchar(20),
meet_name varchar(255),
meet_date date
);

drop table results

create table results (
meet_code varchar(20),
meet_name varchar(255),
meet_year varchar(4),
meet_city varchar(50),
course varchar(3),
date date,
distance varchar(20),
event_gender varchar(1),
age_group varchar(10),
athlete_name varchar(255),
athlete_id varchar(20),
birthdate date,
birth_year varchar(4),
gender varchar(1),
nation varchar(3),
swrid varchar(20),
license varchar(20),
club_name varchar(255),
place integer,
swimtime varchar(20),
type varchar(20),
row_id varchar(255) primary key
)
