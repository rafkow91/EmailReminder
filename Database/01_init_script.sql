CREATE TABLE books (
	id integer primary key autoincrement,
	title text,
	author text,
	created_at datetime
);

CREATE TABLE users (
	id integer primary key autoincrement,
	name text,
	email text,
	created_at datetime
);

CREATE TABLE hirings (
	id integer primary key autoincrement,
	user_id integer,
	book_id integer,
	created_at datetime,
	returned_to datetime
);
