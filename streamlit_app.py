import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Connect to Snowflake
cnx = st.connection("Snowflake")
session = cnx.session()

st.title("Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

# User name input
name_on_order = st.text_input("Name on Smoothie")
st.write("Name on your smoothie will be:", name_on_order)

# Fetch data
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

# Ingredient selection
ingredients_list = st.multiselect(
    'Choose Up to 5 ingredients:',
    pd_df["FRUIT_NAME"].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        # Show nutrition info
        st.subheader(f"{fruit_chosen} Nutrition Information")
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on.lower())
        
        if fruityvice_response.status_code == 200:
            fv_df = fruityvice_response.json()
            st.json(fv_df)
        else:
            st.warning(f"Could not fetch data for {search_on}")

    # Insert order to Snowflake
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
