# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Title and description
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

# Establish Snowflake connection
cnx = st.connection("Snowflake")
session = cnx.session()

# Input: Customer name
name_on_order = st.text_input("Name on Smoothie")
st.write("Name on your smoothie will be:", name_on_order)

# Fetch fruit options from Snowflake
fruit_options_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Convert to list of fruit names
fruit_names = [row['FRUIT_NAME'] for row in fruit_options_df.collect()]

# Multiselect input
ingredients_list = st.multiselect('Choose Up to 5 ingredients:', fruit_names, max_selections=5)

# When ingredients selected
if ingredients_list:
    # Join ingredients into string
    ingredients_string = ', '.join(ingredients_list)

    # Create SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)

    # Submit button
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
