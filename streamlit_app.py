# Import python packages
import streamlit as st
import requests
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
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen+' '
        st.subheader(fruit_chosen+'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)












    
    # Join ingredients into string
#     ingredients_string = ', '.join(ingredients_list)

#     # Create SQL insert statement
#     my_insert_stmt = f"""
#         INSERT INTO smoothies.public.orders(ingredients, name_on_order)
#         VALUES ('{ingredients_string}', '{name_on_order}')
#     """

#     st.write(my_insert_stmt)

#     # Submit button
#     time_to_insert = st.button('Submit Order')
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")


# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
