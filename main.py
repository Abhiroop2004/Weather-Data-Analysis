import mysql.connector

def connect_sql():
    cnx = mysql.connector.connect(user ='root', password='12345', host='localhost', database='kolkata_weather')
    cursor = cnx.cursor()
    return cursor

def max_temp(cursor):
    pass
