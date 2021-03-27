CREATE TABLE Uzivatel (
login VARCHAR(30) NOT NULL,
jmeno VARCHAR(30) NOT NULL,
prijmeni VARCHAR(30) NOT NULL,
datum_narozeni DATE,
typ	VARCHAR(30) NOT NULL,
PRIMARY KEY (login),
CHECK (typ='garant' OR typ='vedouci' OR typ='student' OR typ='lektor')
);

CREATE TABLE Mistnost (
id INT(6) UNSIGNED AUTO_INCREMENT NOT NULL,
nazev VARCHAR(30) NOT NULL,
typ VARCHAR(30) ,
kapacita INT(3),
PRIMARY KEY (id)
);

CREATE TABLE Kurz (
zkratka VARCHAR(30) NOT NULL,
popis BLOB,
typ VARCHAR(30) ,
tag1 VARCHAR(30) ,
tag2 VARCHAR(30) ,
tag3 VARCHAR(30) ,
cena INT(6) UNSIGNED NOT NULL,
spravuje VARCHAR(30) NOT NULL,
PRIMARY KEY (zkratka),
FOREIGN KEY (spravuje) REFERENCES Uzivatel(login)
);

CREATE TABLE Termin (
id INT(6) UNSIGNED AUTO_INCREMENT NOT NULL,
nazev VARCHAR(30) NOT NULL,
typ VARCHAR(30) ,
popis BLOB ,
hodnoceni INT(3) UNSIGNED,
datum DATE,
vytvoril VARCHAR(30) NOT NULL,
kurz VARCHAR(30) NOT NULL,
CHECK (hodnoceni>=0 AND hodnoceni<=100),
PRIMARY KEY (id),
FOREIGN KEY (vytvoril) REFERENCES Uzivatel(login),
FOREIGN KEY (kurz) REFERENCES Kurz(zkratka)
);


CREATE TABLE Vedouci_Mistnost (
login VARCHAR(30) NOT NULL,
mistnost INT(6) UNSIGNED NOT NULL,
FOREIGN KEY (login) REFERENCES Uzivatel(login),
FOREIGN KEY (mistnost) REFERENCES Mistnost(id)
);

CREATE TABLE Mistnost_Termin (
mistnost INT(6) UNSIGNED NOT NULL,
termin	INT(6) UNSIGNED AUTO_INCREMENT NOT NULL,
cas DATETIME,
FOREIGN KEY (mistnost) REFERENCES Mistnost(id),
FOREIGN KEY (termin) REFERENCES Termin(id)
);

CREATE TABLE Garant_Kurz (
login VARCHAR(30) NOT NULL,
kurz VARCHAR(30) NOT NULL,
FOREIGN KEY (login) REFERENCES Uzivatel(login),
FOREIGN KEY (kurz) REFERENCES Kurz(zkratka)
);

CREATE TABLE Student_Kurz (
login VARCHAR(30) NOT NULL,
kurz  VARCHAR(30) NOT NULL,
FOREIGN KEY (login) REFERENCES Uzivatel(login),
FOREIGN KEY (kurz) REFERENCES Kurz(zkratka)
);
