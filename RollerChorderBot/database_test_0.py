from hashlib import sha256
import mysql.connector
from mysql.connector import Error

#pip3 install mysql-connector-python==8.0.29


def addTuple ( table_name, username, hashcode, link ):
    insertline= """INSERT INTO %s (telegram_id, qr_hash_code, last_link) 
    VALUES 
    ('%s', '%s', '%s') """ % (table_name, sha256(username.encode("UTF-8")).hexdigest(), hashcode, link)
    
    return insertline

def lookForUsername ( table_name, username):
    queryline= """SELECT telegram_id FROM %s WHERE telegram_id = '%s' """ % (table_name,username)
    
    return queryline

def getConnection():
    connection = mysql.connector.connect(host='sql11.freesqldatabase.com',
                                         database='sql11517236',
                                         user='sql11517236',
                                         password='iCGPzMinBH')
    return connection

def close_connection(connection):
    if connection:
        connection.close()

table_name = "RollerChorderDatabaseTable"
username = "645843test_username98923821"
hashusername = sha256(username.encode("UTF-8")).hexdigest()
hex_number = sha256(b"test_hash")
hashcode = hex_number.hexdigest()
link = ""

"""
try:
    connection = getConnection()
    cursor = connection.cursor()
    
    cursor.execute(lookForUsername(table_name,username))
    record = cursor.fetchone() #none se non trova niente
    close_connection(connection)
    print(record)
except (Exception, mysql.connector.Error) as error:
    print("Error while getting data", error)

"""
#CONNECTION
try:
    connection = mysql.connector.connect(host='sql11.freesqldatabase.com',
                                         database='sql11517236',
                                         user='sql11517236',
                                         password='iCGPzMinBH')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
except Error as e:
    print("Error while connecting to MySQL", e)

#TUPLE INSERTION
try:
    connection = mysql.connector.connect(host='sql11.freesqldatabase.com',
                                         database='sql11517236',
                                         user='sql11517236',
                                         password='iCGPzMinBH')

    newTuple = addTuple (table_name, username, hashcode, link )

    print("the new Touple will be:\n ",newTuple)

    cursor = connection.cursor()
    cursor.execute(newTuple)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into %s table"% table_name)

    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into {} table {}".format(table_name,error))

#END CONNECTION
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
