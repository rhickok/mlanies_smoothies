# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruist you want in your custom Smoothie!")

name on order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect("Choose up to 5 ingredients", my_dataframe, max_selections=6)

if ingredients_list:
  ingredients_string = ""

  for fruit_chosen in ingredients_list:
    ingredients_string += '{} '.format(fruit_chosen)

  my_insert_statment = 'insert into smoothies.public.orders(ingredients, name_on_order) values (\'{}\',\'{}\')'.format(ingredients_string, name_on_order)
  time_to_insert = st.button('Submit Oder')

  if time_to_insert:
    session.sql(my_insert_statment).collect()
    st.success('Your Smoothie is ordered, {}!'.format(name_on_order))
