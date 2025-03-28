# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(" :cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie! """)




name_on_order = st.text_input('Name on Smoothie:')
st.write('Name on Smoothie will be:', name_on_order)

# Get active Snowflake session
session = get_active_session()

# Fetch data and convert to a Pandas DataFrame
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# Extract list of fruit names
fruit_list = my_dataframe['FRUIT_NAME'].tolist()

# Multiselect widget
ingredients_list = st.multiselect('Choose up to 5 ingredients:',my_dataframe , max_selections=5)

if ingredients_list:
    # Create a space-separated string of selected ingredients
    ingredients_string = ' '.join(ingredients_list)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+ """"')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    if  time_to_insert:
         session.sql(my_insert_stmt).collect()
         st.success('Your Smoothie is ordered!', icon="✅")



