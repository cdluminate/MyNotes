SQL Note
---

> sqlite.org  
> http://www.w3school.com.cn/sql/index.asp  

# SQL basics

Note, SQL is case insensitive!  

A sql command is like
```
select LastName from Persons
```

SQL contains  
* DML, data manipulation language  
* DDL, data definition language  

DML is like  
* select  
* update  
* delete  
* insert into  

DDL is like  
* create database  
* alter database  
* create table  
* alter table  
* drop table  
* create index  
* drop index  

### SELECT
```
select <colomn_name> from <table_name>
select * from <table_name>

SELECT Firstname, lastname FROM persons
```

### SELECT DISTINCT
```
select distinct <column_name> from <table_name>
```

### WHERE
```
select <column_name> from <table_name> where <column> <operator> <value>

operators:
=  equal
<> inequal
>
<
>=
<=
BETWEEN
LIKE
```
e.g. `select * from Persons where City='Beijing'`

### AND, OR
e.g. `select * from Persons where FirstName='Thomas' and LastName='Carter'`  
e.g. `select * from Persons where FirstName='Thomas' or LastName='Carter'`  
e.g. `SELECT * FROM Persons WHERE (FirstName='Thomas' OR FirstName='William') AND LastName='Carter'`

### ORDER
e.g. `SELECT Company, OrderNumber FROM Orders ORDER BY Company`  
e.g. `SELECT Company, OrderNumber FROM Orders ORDER BY Company, OrderNumber`  
e.g. `SELECT Company, OrderNumber FROM Orders ORDER BY Company DESC`  
e.g. `SELECT Company, OrderNumber FROM Orders ORDER BY Company DESC, OrderNumber ASC`  

### INSERT INTO
```
insert into <table_name> values <value1, value2, ...>
insert into <table_name> (column1, column2, ...) values (<value1, value2, ...>)
```

### UPDATE
```
update <table_name> set <column_name> = <new_value> where <column_name> = <value>
```

### DELETE
```
delete from <table_name> where <column_name> = value
delete * from <table_name>
```

# SQL advanced

### TOP
```
select top <number [percent]> <column_name> from <table_name>
```

### LIKE
```
select <column_name> from <table_name> where <column_name> like <pattern>
select <column_name> from <table_name> where <column_name> not like <pattern>

e.g.
select * from persons where city like 'N%' --> N% matches e.g. 'New York',
  where % is the wildcard. Key word 'not' makes matching samples filtered.
```

### SQL wildcard
```
%                   any char any length
_                   one any char
[charlist]          any one of them
[!charlist]         except any of them
```

### IN
```
select <column_name> from <table_name> where <column_name> in (value1, value2, value3, ...)
```

### BETWEEN
```
select <column_name> from <table_name> where <column_name> between value1 and value2
select <column_name> from <table_name> where <column_name> not between value1 and value2
```

### ALIAS
```
select <column_name> from <table_name> as <table_alias_name>
select <column_name> as <column_alias_name> from <table_name>
```

### JOIN, INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN
todo

### UNION
```
# concat all the uniq results
select <column_name> from <table1> UNION select <column_name> from <table2>
# concat all results
select <column_name> from <table1> UNION ALL select <column_name> from <table2>
```

### SELECT INFO
used for copying.
todo

### CREATE DATABASE
```
create database <database_name>
```

### CREATE TABLE
```
create table <table_name> (
  <column_name1> <type1>,
  <column_name2> <type2>,
  <column_name3> <type3>,
  ...
)
```
types:
```
int(.), smallint(.), tinyint(.), integer(MAX_PLACES)
decimal(size, d), numeric(size, d)
char(size)
varchar(size)
date(yyyymmdd)
```

### CONSTRAINTS

#### NOT NULL
```
create table persons (
  guid int NOT NULL,
  ...
)
```

#### UNIQUE
```
guid int NOT NULL,
...
UNIQUE (guid),
```

#### PRIMARY KEY
```
guid int NOT NULL,
...
PRIMARY KEY (guid),
```

#### FOREIGN KEY
todo

#### CHECK
```
guid int NOT NULL,
CHECK (guid > 0)
```

#### DEFAULT
```
city varchar(255) DEFAULT 'sandnes'

ALTER TABLE Persons
ALTER city DROP DEFAULT
```

### CREATE INDEX
for faster lookup speed.
```
create [unique] index <index_name> ON <table_name> (<column_name> [DESC])
```

### DROP and TRUNCATE
```
DROP INDEX <index_name> ON <table_name>

DROP TABLE <table_name>

DROP DATABASE <database_name>

TRUNCATE TABLE <table_name>
```

### ALTER
```
alter table <table_name> <ADD|DROP|ALTER> <column_name> <datatype|column <column_name>>
```

### AUTO INCREMENT
```
guid int NOT NULL AUTO_INCREMENT,
PRIMARY KEY (guid)
```

### VIEW
todo

### DATE functions
todo, dependent on database implementation

### IS [NOT] NULL
```
select name from persons where name IS NOT NULL
```

### SQL datatype
todo, dependant to database implementation, e.g. sqlite3 `sqlite3-doc`.

## SQL Functions
```
SELECT function(<column_name>) FROM <table_name>
```
lookup concrete implementation documentation for functions in detail.
```
select avg(column_name) from table_name -> average, null is excluded.
select count(column_name) from table_name
select count(*) fron table_name
select count(distinct column_name) from table_name
select first(column_name) from table_name
select last(column_name) from table_name
select max(column_name) from table_name
select min(column_name) from table_name
select sum(column_name) from table_name
       ucase(
       lcase(
       mid(                                 --> string slicing
       len(                                 --> string length
select round(column_name, decimals) from table_name
select column_name, now() from table_name
select format(column_name, format) from table_name

-- group by  and  having
select column_name, SUM(column_name) from table_name group by column_name
```

# SQL quick reference
> http://www.w3school.com.cn/sql/sql_quickref.asp  
