DROP TABLE IF EXISTS shelfie;
CREATE TABLE shelfie
	(
	isbn bigint PRIMARY KEY,
	title varchar(255) DEFAULT NULL,
	name_first varchar(255) DEFAULT NULL,
	name_last varchar(255) DEFAULT NULL,
	publisher varchar(255) DEFAULT NULL,
	date_publication date DEFAULT NULL,
	binding varchar(255) DEFAULT NULL,
	notes varchar DEFAULT NULL,
	date_created date NOT NULL DEFAULT current_timestamp,
	date_updated date DEFAULT NULL
	);