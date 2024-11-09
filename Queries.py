import pandas

def dynamic(cursorObject, day, monthNo):
    queryList = []
    response = []
    tail = f''' from weather where Day(`Date time`)={day} and Month(`Date Time`)={monthNo};'''
    
    queryList.append("select avg(`Maximum Temperature`)")
    queryList.append("select avg(`Minimum Temperature`)")
    queryList.append("select max(`Maximum Temperature`)")
    queryList.append("select min(`Minimum Temperature`)")
    queryList.append("select avg(`Precipitation`)")
    queryList.append("select max(`Precipitation`)")

    for query in queryList:
        cursorObject.execute(query+tail)
        response.append(round(cursorObject.fetchall()[0][0],2))

    response = pandas.DataFrame(response, columns=[''], index= ['Average Max Temp', 'Average Min Temp', 'Max Recorded Temp', 'Min Recorded Temp', 'Average Rainfall', 'Max Rainfall'])#, 'Conditions Summary'])
    return response

def conditions_summary(cursorObject, day, monthNo):
    df= pandas.DataFrame(index=[''])

    query = f'''select Conditions, count(Conditions) from weather where Day(`Date time`)={day} and Month(`Date Time`)={monthNo} group by Conditions'''
    cursorObject.execute(query)
    response = cursorObject.fetchall()

    for condition in ['Clear', 'Partially cloudy', 'Rain', 'Overcast']:
        sum =0
        for label in response:
            if condition in label[0]:
                sum+= label[1]
        if sum:
            df[condition] = [f"{sum} out of last 6 years "]
        
    return df

    
def static_table(cursorObject):
    dataframe = pandas.DataFrame(index= ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Year'])

    query = '''select min(`Minimum Temperature`) from weather group by month(`Date Time`);'''
    cursorObject.execute(query)
    response = cursorObject.fetchall()
    response = [temp[0] for temp in response]
    response.append(min(response))
    dataframe['Min. Recorded Temperature'] =response

    query = '''select avg(`Temperature`) from weather group by month(`Date Time`);'''
    cursorObject.execute(query)
    response = cursorObject.fetchall()
    response = [temp[0] for temp in response]
    response.append(sum(response)/len(response))
    dataframe['Average Temperature'] =response

    query = '''select max(`Maximum Temperature`) from weather group by month(`Date Time`);'''
    cursorObject.execute(query)
    response = cursorObject.fetchall()
    response = [temp[0] for temp in response]
    response.append(max(response))
    dataframe['Max. Recorded Temperature'] =response

    query = '''select sum(`Precipitation`)/6 from weather group by month(`Date Time`);'''
    cursorObject.execute(query)
    response = cursorObject.fetchall()
    response = [temp[0] for temp in response]
    response.append(sum(response))
    dataframe['Average Rainfall'] =response

    query = '''select count(*)/6 from weather where Precipitation>0 group by Month(`Date time`);'''
    cursorObject.execute(query)
    response = cursorObject.fetchall()
    response = [float(temp[0]) for temp in response]
    response.append(sum(response))
    dataframe['Average Rainy Days'] =response

    query = '''select avg(`Relative Humidity`) from weather group by month(`Date Time`);'''
    cursorObject.execute(query)
    response = cursorObject.fetchall()
    response = [temp[0] for temp in response]
    response.append(sum(response)/len(response))
    dataframe['Average Rel. Humidity'] =response

    return dataframe
