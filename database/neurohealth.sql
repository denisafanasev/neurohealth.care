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