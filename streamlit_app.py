# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import requests

# ----- Snowflake Connection -----
# Replace these with your actual Snowflake credentials or Streamlit Secrets
connection_parameters = {
    "account": "GLZCOCF-FXB69329",
    "user": "Sri12345",
    "password": "Srilakshmi@2003",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC"
}

session = Session.builder.configs(connection_parameters).create()

# ----- UI -----
st.title("Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Load fruit options from Snowflake
fruit_df = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
           .select("FRUIT_NAME")
           .to_pandas()
)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_df["FRUIT_NAME"].tolist(),
    max_selections=5
)

if ingredients_list and name_on_order:

    ingredients_string = ", ".join(ingredients_list)

    # 🔹 Example: show info for one fruit (watermelon)
    smoothiefroot_response = requests.get(
        "https://my.smoothiefroot.com/api/fruit/watermelon"
    )

    if smoothiefroot_response.status_code == 200:
        st.subheader("Fruit Nutrition Info 🍉")
        st.dataframe(
            smoothiefroot_response.json(),
            use_container_width=True
        )

    sql_to_run = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}');
    """

    submit = st.button("Submit Order")

    if submit:
        session.sql(sql_to_run).collect()
        st.success("Your Smoothie is ordered! ✅")

else:
    st.info("Enter your name and pick ingredients to continue.")
