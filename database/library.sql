CREATE DATABASE library_db;

USE library_db;

CREATE TABLE admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    book_name VARCHAR(200),
    author VARCHAR(200),
    category VARCHAR(100),
    quantity INT
);