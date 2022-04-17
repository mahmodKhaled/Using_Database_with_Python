CREATE TABLE Ages (
   name VARCHAR (128),
   age INTEGER

)

DELETE FROM Ages;
INSERT INTO Ages (name, age) VALUES ('Mallissaa', 26);
INSERT INTO Ages (name, age) VALUES ('Codi', 28);
INSERT INTO Ages (name, age) VALUES ('Ezekiel', 33);
INSERT INTO Ages (name, age) VALUES ('Fiza', 28);

SELECT hex(name || age) AS X FROM Ages ORDER BY X
the result is : 436F64693238