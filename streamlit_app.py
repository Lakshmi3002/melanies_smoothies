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
# Load fruit options
# ✅ Snowpark → Pandas (ONCE)
# -----------------------------
pd_df = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
           .select(col("FRUIT_NAME"), col("SEARCH_ON"))
           .to_pandas()
)

# Optional debug
st.dataframe(pd_df)

# -----------------------------
# Ingredient Selector
# -----------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"].tolist(),
    max_selections=5
)

# -----------------------------
# Process Selection
# -----------------------------
if ingredients_list and name_on_order:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:

        ingredients_string += fruit_chosen + " "

        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]

        st.subheader(f"{fruit_chosen} Nutrition Information")

        response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        )

        if response.status_code == 200:
            st.dataframe(response.json(), use_container_width=True)
        else:
            st.error("Nutrition data not found.")

    insert_sql = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}');
    """

    if st.button("Submit Order"):
        session.sql(insert_sql).collect()
        st.success("Your Smoothie is ordered! ✅")

else:
    st.info("Enter your name and pick ingredients to continue.")
