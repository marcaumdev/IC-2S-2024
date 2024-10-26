CREATE DATABASE BD_Clima_Saude;

USE BD_Clima_Saude;

CREATE TABLE pais(
	id INT UNIQUE AUTO_INCREMENT,
    nome VARCHAR(100),
    sigla VARCHAR(5),
    densidade INT,
    area FLOAT,
    
    PRIMARY KEY (id)
);

CREATE TABLE mortes(
	id INT UNIQUE AUTO_INCREMENT,
    id_pais INT,
    ano INT,
    quantidade INT,
    
    PRIMARY KEY (id),
    FOREIGN KEY (id_pais) REFERENCES pais(id)
);

CREATE TABLE emissao(
	id INT UNIQUE AUTO_INCREMENT,
    id_pais INT,
    ano INT,
    total FLOAT,
    carvao FLOAT,
    petroleo FLOAT,
    gas FLOAT,
    cimento FLOAT,
    queima FLOAT,
    outros FLOAT,
    
    PRIMARY KEY (id),	
    FOREIGN KEY (id_pais) REFERENCES pais(id)
);

CREATE TABLE temperatura(
	id INT UNIQUE AUTO_INCREMENT,
    id_pais INT,
    ano INT,
    indice DECIMAL(10,2),
    
    PRIMARY KEY (id),
    FOREIGN KEY (id_pais) REFERENCES pais(id)
);

SELECT * FROM pais;