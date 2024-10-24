CREATE DATABASE BD_Clima_Saude;

USE BD_Clima_Saude;

CREATE TABLE continente(
	id INT UNIQUE AUTO_INCREMENT,
    nome VARCHAR(100),
    sigla VARCHAR(5),
    
    PRIMARY KEY (id)
);

CREATE TABLE causa(
	id INT UNIQUE AUTO_INCREMENT,
    causa VARCHAR(100),
    
    PRIMARY KEY (id)
);

CREATE TABLE pais(
	id INT UNIQUE AUTO_INCREMENT,
    id_continente INT,
    nome VARCHAR(100),
    sigla VARCHAR(5),
    litoraneo BOOLEAN,
    ano YEAR,
    
    PRIMARY KEY (id),
    FOREIGN KEY (id_continente) REFERENCES continente(id)
);

CREATE TABLE mortes(
	id INT UNIQUE AUTO_INCREMENT,
    id_causa INT,
    id_pais INT,
    ano YEAR,
    quantidade INT,
    
    PRIMARY KEY (id),
    FOREIGN KEY (id_causa) REFERENCES causa(id),
    FOREIGN KEY (id_pais) REFERENCES pais(id)
);

CREATE TABLE temperatura(
	id INT UNIQUE AUTO_INCREMENT,
    id_pais INT,
    ano YEAR,
    indice DECIMAL(10,2),
    umidade DECIMAL(10,2),
    
    PRIMARY KEY (id),
    FOREIGN KEY (id_pais) REFERENCES pais(id)
);

CREATE TABLE poluicao(
	id INT UNIQUE AUTO_INCREMENT,
    id_pais INT,
    ano YEAR,
    agua DECIMAL(10,2),
    ar DECIMAL(10,2),
    co2 DECIMAL(10,2),
    
    PRIMARY KEY (id),
    FOREIGN KEY (id_pais) REFERENCES pais(id)
);