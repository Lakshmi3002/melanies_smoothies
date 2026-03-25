# -----------------------------
# Imports
# -----------------------------
import streamlit as st
import requests
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# -----------------------------
# Snowflake Connection
# -----------------------------
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

# -----------------------------
# UI
# -----------------------------
st.title("Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie:")

# -----------------------------
# Load Fruit Options
# -----------------------------
fruit_df = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
           .select(col("FRUIT_NAME"), col("SEARCH_ON"))
           .to_pandas()
)

# -----------------------------
# Ingredient Selector
# -----------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_df["FRUIT_NAME"].tolist(),
    max_selections=5
)

# -----------------------------
# Process Selection
# -----------------------------
if ingredients_list and name_on_order:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:

        ingredients_string += fruit_chosen + " "

        # ✅ Get SEARCH_ON value for API
        search_on = fruit_df.loc[
            fruit_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        st.write(
            f"Search value for **{fruit_chosen}** is **{search_on}**"
        )

        # ✅ Call external API using SEARCH_ON
        st.subheader(f"{fruit_chosen} Nutrition Information")

        response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        )

        if response.status_code == 200:
            st.dataframe(response.json(), use_container_width=True)
        else:
            st.error("Nutrition data not found.")

    # -----------------------------
    # Insert Order
    # -----------------------------
    insert_sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}');
    """

    submit = st.button("Submit Order")

    if submit:
        session.sql(insert_sql).collect()
        st.success("Your Smoothie is ordered! ✅")

else:
    st.info("Enter your name and pick ingredients to continue.")
