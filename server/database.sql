CREATE DATABASE stockprices;

CREATE TABLE twoweekprices(
    stock_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price1 INT,
    price3 INT,
    price4 INT,
    price5 INT,
    price6 INT,
    price2 INT,
    price7 INT,
    price8 INT,
    price9 INT,
    price10 INT,
    price11 INT,
    price12 INT,
    price13 INT,
    price14 INT
);

INSERT INTO twoweekprices (name, price1, price2, price3, price4, price5, price6, price7, price8, price9, price10, price11, price12, price13, price14) 
VALUES ('nice', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14);