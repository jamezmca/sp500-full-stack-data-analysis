CREATE DATABASE stockprices;

CREATE TABLE twoweekprices(
    stock_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    lastFetched DATE,
    prices VARCHAR
);

INSERT INTO twoweekprices (name, ) 
VALUES ('nice', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14);

INSERT INTO table_name (column_list)
VALUES
    (value_list_1),
    (value_list_2),
    ...
    (value_list_n);