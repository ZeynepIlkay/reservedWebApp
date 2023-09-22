import mysql.connector
from mysql.connector import pooling



connection_pool = pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=30,
    user ='rezuser',
    password='database',
    host='mariadb.01',
    database='reservation',
    port=3306,
)









'''import mysql.connector


mysqldb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="database2022",
    database="reservations"
)
    user ='rezuser',
    password='database',
    host='mariadb.01',
    database='reservation',

def get_db_connection():
    return mysqldb '''