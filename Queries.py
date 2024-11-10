import pandas

def dynamic(cursorObject, day, monthNo):
    query=f'''select avg(`Maximum Temperature`), avg(`Minimum Temperature`),
            max(`Maximum Temperature`), min(`Minimum Temperature`),
            avg(`Precipitation`), max(`Precipitation`)
            from weather where Day(`Date time`)={day} and Month(`Date Time`)={monthNo};'''

    cursorObject.execute(query)
    df = pandas.DataFrame(cursorObject.fetchall()[0], columns=[''],
                index= ['Average Max Temp', 'Average Min Temp', 'Max Recorded Temp', 'Min Recorded Temp', 'Average Rainfall', 'Max Rainfall'])
    return df


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
