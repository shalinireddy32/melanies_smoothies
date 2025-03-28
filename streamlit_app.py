# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(" :cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Get user input
name_on_order = st.text_input('Name on Smoothie:')
st.write('Name on Smoothie will be:', name_on_order)

# Get active Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch data and convert to a Pandas DataFrame
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# Extract list of fruit names
fruit_list = my_dataframe['FRUIT_NAME'].tolist()

# Multiselect widget
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_list, max_selections=5)

if ingredients_list:
    # Create a space-separated string of selected ingredients
    ingredients_string = ' '.join(ingredients_list)

    # Loop to fetch fruit nutrition info
    for fruit_chosen in ingredients_list:
        st.subheader(fruit_chosen + ' Nutrition Information')
        
        # API request to fetch nutrition data
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
        
        if smoothiefroot_response.status_code == 200:
            st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        else:
            st.write(f"Could not fetch nutrition info for {fruit_chosen}.")
    
    # SQL Insert Statement
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                         VALUES ('{ingredients_string}', '{name_on_order}')"""

    # Display query (optional)
    st.write(my_insert_stmt)





