import mysql.connector
from mysql.connector import errorcode


DB_NAME = 'warhammer'

TABLES = {}

TABLES['OrkShop'] = (
  "CREATE TABLE `warhammer`.`OrkShop` ("
  " `id` INT NOT NULL AUTO_INCREMENT,"
  " `new` VARCHAR(45) NOT NULL,"
  " `new2int` INT NULL,"
  " PRIMARY KEY (`id`))"
)

#TABLES['OrkShop'] = (
#  "CREATE TABLE 'OrkShop' ("
#  "  'title' varchar(255) NOT NULL,"
#  "  'price' int(7) NOT NULL,"
#  "  'status' varchar(255) NOT NULL,"
#  "  'url' varchar(255) NOT NULL,"
#  ") ENGINE=InnoDB")

#TABLES['HobbyGames'] = (
#  "CREATE TABLE 'OrkShop' ("
#  "  'title' varchar(255) NOT NULL,"
#  "  'price' int(7) NOT NULL,"
#  "  'status' varchar(255) NOT NULL,"
#  "  'url' varchar(255) NOT NULL,"
#  ") ENGINE=InnoDB")

config = {
  'user': 'root',
  'password': '',
  'host': '192.168.56.1',
  'database': 'warhammer',
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        print(table_description)
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

create_database(cursor)

cursor.close()
cnx.close()