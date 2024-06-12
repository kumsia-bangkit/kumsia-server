create table users(
	id varchar(36) not null primary key,
	username varchar(255) not null,
	password varchar(255) not null,
	first_name varchar(255) not null,
	last_name varchar(255) not null,
	dob date not null,
	roles varchar(255) not null,
	gender varchar(255) not null
);