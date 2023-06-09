import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#DISPLAY BREAKFAST MENU
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')

#BUILD YOUR OWN SMOOTHIE
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#IMPORT FRUIT LIST FROM UNI LIST
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#CREATE A PICK LIST FROM UNI LIST
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#DISPLAY UNI LIST CHOICE IN TABLE
streamlit.dataframe(fruits_to_show)

#IMPORT FRUITY VICE DATA
streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

#DISPLAY FRUITY VICE CHOICE IN TABLE
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#NORMALIZE THE DATA FOR DISPLAY
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#DISPLAY THE DATAFRAME
streamlit.dataframe(fruityvice_normalized)


streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_rows)


fruit_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice)
my_cure.execute("insert into fruit_load_list values ('from streamlit')")
