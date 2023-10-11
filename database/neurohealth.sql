create table users(
	doc_id INT PRIMARY KEY,
	login VARCHAR ( 15 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ),
	email VARCHAR ( 50 ) UNIQUE NOT NULL,
	role VARCHAR ( 15 ) NOT NULL,
	name VARCHAR ( 50 ) NOT NULL,
	created_date TIMESTAMP NOT NULL,
	education_module_expiration_date TIMESTAMP NOT NULL,
	probationers_number INT NOT NULL,
	active BOOLEAN DEFAULT FALSE,
	email_confirmed BOOLEAN DEFAULT FALSE,
	token VARCHAR ( 255 )
);

create table action(
	doc_id INT PRIMARY KEY,
	user_id INT NOT NULL,
	action VARCHAR ( 200 ) NOT NULL,
	comment_action VARCHAR ( 250 ) NOT NULL,
	created_date TIMESTAMP NOT NULL
);

create table courses_list(
    doc_id INT PRIMARY KEY,
    name VARCHAR ( 150 ) NOT NULL,
    description TEXT NOT NULL,
    type VARCHAR ( 20 ) NOT NULL,
    image VARCHAR ( 200 ) NOT NULL
);

create table modules(
    doc_id INT PRIMARY KEY,
    id_course INT NOT NULL,
    name VARCHAR ( 150 ) NOT NULL
);

create table lessons(
    doc_id INT PRIMARY KEY,
    id_module INT NOT NULL,
    name VARCHAR ( 150 ) NOT NULL,
    materials VARCHAR ( 100 ) [] ,
    task TEXT NULL,
    text TEXT NULL,
    link jsonb []
);