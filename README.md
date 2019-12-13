# BigData Analysis - Instacart

## Dataset

The dataset used in this project is available at [Instacart](https://www.instacart.com/datasets/grocery-shopping-2017)


## Data Preparation

Let's connect to the cluster and  start by downloading and extracting the dataset:

```shell
ssh czechflek@hador.ics.muni.cz
wget https://s3.amazonaws.com/instacart-datasets/instacart_online_grocery_shopping_2017_05_01.tar.gz
mv instacart_online_grocery_shopping_2017_05_01.tar.gz\?X-Amz-Expires\=21600  instacart.tar.gz
tar xfz instacart.targ.gz -C data
```

The next step is to transfer the dataset to Hadoop and rename it for convenience:

```shell
 hdfs dfs -put /storage/brno2/home/czechflek/projekt/data/instacart_2017_05_01/
 hdfs dfs -mv instacart_2017_05_01 instacart
 ```

Since we will need each CSV in its own separate folder, we need to create them on HDF and move the files accordingly:

```shell
 hdfs dfs -mkdir instacart/aisles
 hdfs dfs -mv instacart/aisles.csv instacart/aisles/
 # ...and so on
 ```

## Organizing Data in Hive

 Before we can start analysing data, we need to load the datasets to Hive. 

We use the following command to connect to Hive:

 ```shell
 beeline -u "jdbc:hive2://hador-c1.ics.muni.cz:10000/default;principal=hive/hador-c1.ics.muni.cz@ICS.MUNI.CZ"
 ```

Now we can create a new database called `instacart`

```hql
CREATE DATABASE IF NOT EXISTS instacart;
USE instacart;
```

 Since we already loaded all CSVs on the HDFS, we can begin working on creating an external table.

### Tables

#### Aisles

|   Field     | Datatype |
|   -------:  | :------- |
|   aisle_id  |   INT    |
|   aisle     |  STRING  |

Create an external table `aisles__ext`:

```hql
CREATE EXTERNAL TABLE IF NOT EXISTS aisles__ext (
    aisle_id INT,
    aisle STRING)
ROW FORMAT
    DELIMITED FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/user/czechflek/instacart/aisles'
tblproperties("skip.header.line.count"="1");
```

Create an optimized parquet table with snappy compression:

```hql
CREATE TABLE IF NOT EXISTS aisles (
    aisle_id INT,
    aisle STRING)
STORED AS PARQUET
tblproperties("parquet.compression"="SNAPPY");
```

Now we can load the data into the new table and drop the external one:

```hql
INSERT OVERWRITE TABLE aisles
SELECT
    aisle_id,
    aisle
FROM aisles__ext;

DROP TABLE aisles__ext;
```

#### Departments

|   Field          | Datatype |
|   ------------:  | :------- |
|   department_id  |   INT    |
|   department     |  STRING  |

Create an external table `departments__ext`:

```hql
CREATE EXTERNAL TABLE IF NOT EXISTS departments__ext (
    department_id INT,
    department STRING)
ROW FORMAT
    DELIMITED FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/user/czechflek/instacart/departments'
tblproperties("skip.header.line.count"="1");
```

Create an optimized parquet table with snappy compression:

```hql
CREATE TABLE IF NOT EXISTS departments (
    department_id INT,
    department STRING)
STORED AS PARQUET
tblproperties("parquet.compression"="SNAPPY");
```

Now we can load the data into the new table and drop the external one:

```hql
INSERT OVERWRITE TABLE departments
SELECT
    department_id,
    department
FROM departments__ext;

DROP TABLE departments__ext;
```

#### Products

|   Field          | Datatype |
|   ------------:  | :------- |
|   product_id     |   INT    |
|   product_name   |  STRING  |
|   aisle_id       |   INT    |
|   department_id  |   INT    |

Create an external table `products__ext`:

```hql
CREATE EXTERNAL TABLE IF NOT EXISTS products__ext (
    product_id INT,
    product_name STRING,
    aisle_id INT,
    department_id INT)
ROW FORMAT
    DELIMITED FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/user/czechflek/instacart/products'
tblproperties("skip.header.line.count"="1");
```

Create an optimized parquet table with snappy compression:

```hql
CREATE TABLE IF NOT EXISTS products (
    product_id INT,
    product_name STRING,
    aisle_id INT,
    department_id INT)
STORED AS PARQUET
tblproperties("parquet.compression"="SNAPPY");
```

Now we can load the data into the new table and drop the external one:

```hql
INSERT OVERWRITE TABLE products
SELECT
    product_id,
    product_name,
    aisle_id,
    department_id
FROM products__ext;

DROP TABLE products__ext;
```

#### Orders

|   Field                   | Datatype |
|   ------------:           | :------- |
|   order_id                |    INT   |
|   user_id                 |    INT   |
|   eval_set                |  STRING  |
|   order_number            |    INT   |
|   order_dow               |    INT   |
|   order_hour_of_day       |    INT   |
|   days_since_prior_order  |  FLOAT   |

Create an external tablee `orders__ext`:

```hql
CREATE EXTERNAL TABLE IF NOT EXISTS orders__ext (
    order_id INT,
    user_id INT,
    eval_set STRING,
    order_number INT,
    order_dow INT,
    order_hour_of_day INT,
    days_since_prior_order FLOAT)
ROW FORMAT
    DELIMITED FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/user/czechflek/instacart/orders'
tblproperties("skip.header.line.count"="1");
```

Create an optimized parquet table with snappy compression:

```hql
CREATE TABLE IF NOT EXISTS orders (
    order_id INT,
    user_id INT,
    eval_set STRING,
    order_number INT,
    order_dow INT,
    order_hour_of_day INT,
    days_since_prior_order FLOAT)
STORED AS PARQUET
tblproperties("parquet.compression"="SNAPPY");
```

Now we can load the data into the new table and drop the external one:

```hql
INSERT OVERWRITE TABLE orders
SELECT
    order_id,
    user_id,
    eval_set,
    order_number,
    order_dow,
    order_hour_of_day,
    days_since_prior_order
FROM orders__ext;

DROP TABLE orders__ext;
```

#### Order - Products

|   Field                   | Datatype |
|   ------------:           | :------- |
|   order_id                |    INT   |
|   product_id              |    INT   |
|   add_to_cart_order       |    INT   |
|   reordered               |    INT   |

Create an external table `order_products__ext`:

```hql
CREATE EXTERNAL TABLE IF NOT EXISTS order_products__ext (
    order_id INT,
    product_id INT,
    add_to_cart_order INT,
    reordered INT)
ROW FORMAT
    DELIMITED FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/user/czechflek/instacart/order_products'
tblproperties("skip.header.line.count"="1");
```

Create an optimized parquet table with snappy compression:

```hql
CREATE TABLE IF NOT EXISTS order_products (
    order_id INT,
    product_id INT,
    add_to_cart_order INT,
    reordered INT)
STORED AS PARQUET
tblproperties("parquet.compression"="SNAPPY");
```

Now we can load the data into the new table and drop the external one:

```hql
INSERT OVERWRITE TABLE order_products
SELECT
    order_id,
    product_id,
    add_to_cart_order,
    reordered
FROM order_products__ext;

DROP TABLE order_products__ext;
```

## Data Analysis

### Top 5 Categories

Since there is no category field, we are going to use `aisles` as our categories.
To determine the most popular ones, we need to join `order_products` with `products` and then again with `aisles`. After that, we group the newly joined table by aisles and extract the top 5.

```hql
SELECT COUNT(*) as Number_of_Products, A.aisle as Category
FROM order_products
    LEFT JOIN products
        ON order_products.product_id = products.product_id
    LEFT JOIN aisles as A
        ON products.aisle_id = A.aisle_id
GROUP BY A.aisle
ORDER BY Number_of_Products DESC
LIMIT 5;
```

The query above results in the following output:

```text
+---------------------+-----------------------------+--+
| number_of_products  |           category          |
+---------------------+-----------------------------+--+
| 3787048             | fresh fruits                |
| 3510733             | fresh vegetables            |
| 1778128             | packaged vegetables fruits  |
| 1449684             | yogurt                      |
| 1005632             | packaged cheese             |
+---------------------+-----------------------------+--+
```

### Top 10 Products

To determine the most popular products, we need to join `order_products` with `products`. Then that, we simply group the newly joined table by profucts and extract the top 5.

```hql
SELECT COUNT(*) as Number_of_Orders, P.product_name as Product
FROM order_products
    LEFT JOIN products as P
        ON order_products.product_id = P.product_id
GROUP BY P.product_name
ORDER BY Number_of_Orders DESC
LIMIT 10;
```

The query above results in the following output:

```text
+-------------------+-------------------------+--+
| number_of_orders  |         product         |
+-------------------+-------------------------+--+
| 491291            | Banana                  |
| 394930            | Bag of Organic Bananas  |
| 275577            | Organic Strawberries    |
| 251705            | Organic Baby Spinach    |
| 220877            | Organic Hass Avocado    |
| 184224            | Organic Avocado         |
| 160792            | Large Lemon             |
| 149445            | Strawberries            |
| 146660            | Limes                   |
| 142813            | Organic Whole Milk      |
+-------------------+-------------------------+--+
```