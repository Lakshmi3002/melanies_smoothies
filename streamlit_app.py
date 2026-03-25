# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

# Title
st.title(f"Customize Your Smoothie! :balloon: {st.__version__}")
st.write("Choose the fruits you want in your custom smoothie!")

# User enters name
name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your smoothie will be:', name_on_order)

# Snowflake session from Streamlit
session = get_active_session()

# Load ingredient list from Snowflake
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
           .select(col("FRUIT_NAME"))
           .to_pandas()
)

# Multiselect lets the user pick up to 5 fruit names
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe["FRUIT_NAME"].tolist(),
    max_selections=5
)

# Only run insert logic if user selected ingredients
if ingredients_list and name_on_order:

    # Construct ingredient string
    ingredients_string = ", ".join(ingredients_list)

    # Build SQL insert safely
    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}');
    """

    # Show user the SQL (optional debugging)
    st.write("Order Preview:", my_insert_stmt)

    # Button to confirm submission
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered! ✅")

else:
    st.info("Pick at least one ingredient and enter your name to continue.")


import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)
