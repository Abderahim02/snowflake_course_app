# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose your custom fruites")

from snowflake.snowpark.functions import col


name = st.text_input("Name of the Smoothie")
st.write("The name that appears in the smoothie is: ", name)
session = get_active_session() 
data= session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data = data, use_container_width = True) 


ingredients_list = st.multiselect(
"Choose fruits to ilculde in the smoothie, up to 5 ingredients :",
    data,
    max_selections = 5
    
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ' '.join(ingredients_list)
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + "','" + name+ """')"""

    st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

