# Big Data Analysis - Instacart

## Data Preparation

After we connect to the cluster, we start by downloading and extracting the dataset:

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

HQL script which creates an external table `aisles`:

```hql
CREATE EXTERNAL TABLE IF NOT EXISTS aisles (
    aisle_id INT,
    aisle STRING)
ROW FORMAT
    DELIMITED FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/user/czechflek/instacart/aisles'
tblproperties("skip.header.line.count"="1");
```

#### Departments

|   Field          | Datatype |
|   ------------:  | :------- |
|   department_id  |   INT    |
|   department     |  STRING  |

HQL script which creates an external table `departments`:

```hql
CREATE EXTERNAL TABLE IF NOT EXISTS departments (
    department_id INT,
    department STRING)
ROW FORMAT
    DELIMITED FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/user/czechflek/instacart/departments'
tblproperties("skip.header.line.count"="1");
```

#### Products

|   Field          | Datatype |
|   ------------:  | :------- |
|   product_id     |   INT    |
|   product_name   |  STRING  |
|   aisle_id       |   INT    |
|   department_id  |   INT    |

HQL script which creates an external table `products`:

```hql
CREATE EXTERNAL TABLE IF NOT EXISTS products (
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

HQL script which creates an external table `orders`:

```hql
CREATE EXTERNAL TABLE IF NOT EXISTS orders (
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
