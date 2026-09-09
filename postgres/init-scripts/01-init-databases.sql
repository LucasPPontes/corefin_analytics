-- Criar banco de dados principal unico 'corefin'
CREATE DATABASE corefin;

-- Conectar no banco corefin e criar os schemas Medallion
\c corefin

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
