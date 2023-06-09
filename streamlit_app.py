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


#CREATE THE REPEATABLE CODE BLOCK (CALLED A FUNCTION)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)     
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#IMPORT FRUITY VICE DATA
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
        
except URLError as e:   
  streamlit.error()  
  
#streamlit.stop()

streamlit.header("The fruit load list contains")
#SNOWFLAKE-RELATED FUNCTIONS
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

#ADD A BUTTON TO LOAD THE FRUIT
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)


fruit_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice)
my_cure.execute("insert into fruit_load_list values ('from streamlit')")
