def dynamic( day = 1, monthNo = 1, cursorObject = None, dataframe = None):
    tail = f''' from weather where Day(`Date time`)={day} and Month(`Date Time`)={monthNo};'''
    
    query= f'''select avg(`Maximum Temperature`)''' + tail
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    #print("\nhhh  ",result[0][0])
    dataframe['Average Max Temp'] = result[0]

    query= f'''select avg(`Minimum Temperature`)''' + tail
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    dataframe['Average Min Temp'] = round(result[0][0], 2)

    query = f'''select max(`Maximum Temperature`)''' + tail
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    dataframe['Max Recorded Temp'] = round(result[0][0], 2)

    query = f'''select min(`Minimum Temperature`)''' + tail
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    dataframe['Min Recorded Temp'] = round(result[0][0], 2)

    query = f'''select avg(`Precipitation`)''' + tail
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    dataframe['Average Rainfall'] = round(result[0][0], 2)

    query = f'''select max(`Precipitation`)''' + tail
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    dataframe['Max Rainfall'] = float(round(result[0][0], 2))
    return dataframe
    query = f'''select count(*) from weather where Day(`Date time`)={day} and Month(`Date Time`)={monthNo} group by Conditions'''
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    #dataframe['Conditions Summary'] = result

    
    #return round(result[0][0], 2)

def static_table(cursorObject = None, dataframe = None):
    query = '''select min(`Minimum Temperature`) from weather group by month(`Date Time`);'''
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    result = [round(temp[0],2) for temp in result]
    result.append(min(result))
    dataframe['Min. Recorded Temperature']= result

    query = '''select avg(`Temperature`) from weather group by month(`Date Time`);'''
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    result = [round(temp[0],2) for temp in result]
    result.append(round(sum(result)/len(result),2))
    dataframe['Average Temperature'] = result

    query = '''select max(`Maximum Temperature`) from weather group by month(`Date Time`);'''
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    result = [round(temp[0],2) for temp in result]
    result.append(max(result))
    dataframe['Max. Recorded Temperature'] = result

    query = '''select sum(`Precipitation`)/6 from weather group by month(`Date Time`);'''
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    result = [round(temp[0],2) for temp in result]
    result.append(sum(result))
    dataframe['Average Rainfall'] = result

    query = '''select count(*)/6 from weather where Precipitation>0 group by Month(`Date time`);'''
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    result = [round(temp[0],2) for temp in result]
    result.append(sum(result))
    dataframe['Average Rainy Days']= result

    query = '''select avg(`Relative Humidity`) from weather group by month(`Date Time`);'''
    cursorObject.execute(query)
    result = cursorObject.fetchall()
    result = [round(temp[0],2) for temp in result]
    result.append(round(sum(result)/len(result),2))
    dataframe['Average Rel. Humidity'] = result

    return dataframe