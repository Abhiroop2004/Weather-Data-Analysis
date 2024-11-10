import mysql.connector, pandas, toml
import streamlit as st
from datetime import datetime
import Queries as Q

def edit_background(file_path, bg, secondary_bg, text):
    with open(file_path, 'r') as file:
        config = toml.load(file)
    config['theme']['backgroundColor'] = bg
    config['theme']['secondaryBackgroundColor'] = secondary_bg
    config['theme']['textColor'] = text
    with open(file_path, 'w') as file:
        toml.dump(config, file)

    print("Background color updated successfully!")

cnx = mysql.connector.connect(user ='root', password='12345', host='localhost', database='kolkata_weather')
cursor = cnx.cursor()
current_time = datetime.now()
hour = current_time.hour
emoji = ""
if (hour >= 18 or hour < 6):
    edit_background(file_path=".streamlit\config.toml", bg="#102b61", secondary_bg="#061024", text="ffffff")
    emoji = "🌃"
else:
    edit_background(file_path=".streamlit\config.toml", bg="#e8cd1e", secondary_bg="#e0ce55", text="#141414")
    emoji = "🌅"

def main():
    st.set_page_config(layout="wide")
    st.title(f"Weather Data Analysis{emoji}")    
    # print(current_time.date)
    navigation_options = ["Home", "Info"]
    menu_selection = st.selectbox("",navigation_options)
    
    if menu_selection == "Home":
        show_home()
    elif menu_selection == "Info":
        show_info()

def show_home():
    st.write("### Climate data for Kolkata from 2017 to 2022")
    table = Q.static_table(cursor)
    st.table(data = table.T.style.format("{:.2f}"))
    column1, column2 = st.columns(2)
    with column1:
        st.write(f"### Historic Data for {current_time.date().strftime('%d %B')}")
        st.dataframe(Q.conditions_summary(cursor, current_time.day, monthNo = current_time.month).T)
    with column2:
        st.dataframe(Q.dynamic(cursor, day=current_time.day, monthNo = current_time.month))

def show_info():
    st.write("# Info")
    st.write("- ### [Abhiroop's LinkedIn](https://linkedin.com/in/abhiroop2004)")
    st.write("- ### [Snehal's LinkedIn](https://www.linkedin.com/in/snehal-ghosh-164a63263)")
    st.write()
    st.write('''Project developed under the guidance of Professor Doctor DeepShubhra Guha Roy
             for the Database Management Systems Laboratory
             being taught by the department of Computer Science and Engineering
             (Artificial Intelligence and Machine Learning) along with 
             Computer Science and Business Studies headed by 
             Professor Amartya Mukherjee at the
             Institute of Engineering and Management SaltLake''')

if __name__ == "__main__":
    main()
