# MiniSQLQueryEngine

To run,

`python sqlengine.py`

**Please enter the path to this directory**

**NOTE -** The main objective was to get all the test cases passing, and the deadline was soon upon us. Hence the coding style has been very bad and there's no documentation.

### Files

- `sqlengine.py` The main file which performs all the processing  
- `parser.py` pyparsing has been used for this `http://pyparsing.wikispaces.com/`  
- `tables.py` File to read in the tables from the specified directory  
- `table1.py`, `table2.py`, `metadata.txt` The database files (Only int values in csv)  

### Types of queries handled
- Select all records : `Select * from table_name;`
- Aggregate functions: Simple aggregate functions on a single column. Sum, average, max and min. They will be very trivial given that the data is only numbers: `select max(col1) from table1;` 
- Project Columns(could be any number of columns) from one or more tables : `Select col1, col2 from table_name;`
- Select/project with distinct from one table : `select distinct(col1), distinct(col2) from table_name;`
- Select with where from one or more tables: `select col1,col2 from table1,table2 where col1 = 10 AND col2 = 20;` In the where queries, there would be a maximum of one AND/OR operator with no NOT operators.
- Projection of one or more(including all the columns) from two tables with one join condition :  
`select * from table1, table2 where table1.col1=table2.col2;`  
`select col1,col2 from table1,table2 where table1.col1 = table2.col2;`  

For the above queries, please note all the permutations and combinations of SQL that MySQL permits, specially when it comes to multiple tables. What is mentioned above are examples of what the queries could be.




`
