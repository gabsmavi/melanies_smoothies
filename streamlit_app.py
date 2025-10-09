# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Configurações de conexão Snowflake
connection_parameters = {
    "account": "<seu_account>",
    "user": "<seu_user>",
    "password": "<sua_senha>",
    "role": "<seu_role>",
    "warehouse": "<seu_warehouse>",
    "database": "smoothies",
    "schema": "public"
}

# Cria a sessão Snowpark
session = Session.builder.configs(connection_parameters).create()

# Streamlit App
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie.")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Puxa frutas do Snowflake (FRUIT_NAME e SEARCH_ON)
my_dataframe = session.table("fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Converte para Pandas DataFrame
pd_df = my_dataframe.to_pandas()
fruits = pd_df['FRUIT_NAME'].tolist()

# Multiselect para escolher frutas
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruits,
    max_selections=5
)

# Mostra informações nutricionais da API usando SEARCH_ON
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)  # Join selected ingredients into a single string
    for fruit_chosen in ingredients_list:
        try:
            # Make API request to get details about each fruit
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
            fruityvice_response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch details for {fruit_chosen}: {str(e)}")


    # mostra lista final de ingredientes
    st.write("Your ingredients:", ingredients_string)
