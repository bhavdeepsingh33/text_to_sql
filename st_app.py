import streamlit as st
# st.set_page_config(layout="wide")
import pandas as pd 
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

from utils import run_sql as rn
from utils import llm_helper as lh
import os

print(os.getcwd())
curr_dir = os.getcwd()
DB_PATH = "t_shirts.db"
CHROMADB_PATH = "chromadb"

st.title("T-Shirts Database Query System")

tab1, tab2 = st.tabs(["Run Query", "Tables"])

with tab2:
    st.subheader("Discounts Table")
    discounts_df = pd.read_csv("tables/discounts_table.csv")
    st.table(discounts_df)

    st.subheader("T-Shirts Table")
    tshirts_df = pd.read_csv("tables/t_shirts_table.csv")
    st.table(tshirts_df)

with tab1:
    question_text = st.text_input("Query")
    run_query = st.button("Run Query")

    if run_query:
        try:
            print("Client Creation Started")
            # client = chromadb.HttpClient()
            client = chromadb.PersistentClient(
                path=CHROMADB_PATH,
                settings=Settings(),
                tenant=DEFAULT_TENANT,
                database=DEFAULT_DATABASE,
            )
            print("Client Created")
            collection = client.get_collection("t_shirts_sql")
            print("Collection Initialized")
        except Exception as e:
            print("Unable to fetch collection from chromadb")
            print(e)
            raise(e)
        else:
            print("Fetching Similar Examples...")
            similar_examples = lh.get_k_similar_queries(question_text, collection)
            print("Similar Examples Fetched")
        # print("similar_examples")
        # print(similar_examples)
        llm = lh.initialize_llm()
        db = lh.connect_SQLDatabase()
        query = lh.get_llm_query(similar_examples, llm, db, question_text)
        # connection = rn.connect_to_database("t_shirts.db")
        # print(question_text)
        query = rn.preprocess_query(query)
        print(query)
        
        output = rn.query_result(DB_PATH, query)
        st.write(f"Query:{question_text}")
        st.write(output)

    # query_text = "How many white Nike tshirts are left in extra small size?"
    # query_text = "total remaining levi white tshirt?"
    # query_text = "How much is the price of all white color levi t shirts?"
    # query_text = "How much is the price of the inventory for all small size t-shirts?"
    # query_text = "How much is the price of all white color levi t shirts?"
    # query_text = "If we have to sell all the Nike’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?"
    # query_text = "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue our store will generate (post discounts)?"
    # query_text = "If we have to sell all the Ven Huson T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?"
    # query_text = "How much revenue  our store will generate by selling all Van Heuson TShirts without discount?"





