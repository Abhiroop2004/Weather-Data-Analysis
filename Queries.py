import mysql.connector, os
from dotenv import load_dotenv

def monthly_temp(aggregator='avg', attribute='Temperature', monthNo=1, year=None):
    cursorObject = cnx.cursor()
    query= f'''select {aggregator}({attribute}) from weather where Month(`Date time`)={monthNo}'''
    if year is not None :
        query+=  f''' and year(`Date time`)={year}'''
    query+= ';'
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    return round(result[0][0], 2)
    
def monthly_rainy_day_count(monthNo=1):
    cursorObject = cnx.cursor()
    query= f''' select avg(days) from(select count(*) as days from weather where Month(`Date time`)={monthNo} and Precipitation>0 group by Year(`Date time`)) as alias;'''
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    return round(result[0][0], 2)

def dynamic(aggregator='avg', attribute='Temperature', day=1, monthNo=None):
    cursorObject = cnx.cursor()
    query= f'''select {aggregator}(`{attribute}`) from weather where Day(`Date time`)={day}'''
    if monthNo is not None :
        query+=  f''' and Month(`Date time`)={monthNo}'''
    query+= ';'
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    return round(result[0][0], 2)

load_dotenv()
mysql_password = os.getenv('mysql_password')

cnx = mysql.connector.connect(user ='root', password=mysql_password, host='localhost', database='kolkata_weather')
print(monthly_temp(attribute='Precipitation', monthNo='6'), 'units')
print(monthly_rainy_day_count(6), 'days')
print(dynamic(aggregator='max', monthNo=4), 'units')
cnx.close()