# import pymysql
import pandas as pd
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
# import chromadb
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt

import utils.prompt as pt
# import utils.run_sql as rn



def initialize_llm():
    from dotenv import load_dotenv
    load_dotenv()
    llm = GoogleGenerativeAI(model="gemini-pro", temperature=0.2)  # google_api_key=api_key,
    return llm

def connect_SQLDatabase():
    db = SQLDatabase.from_uri("sqlite:///t_shirts.db")
    return db

def get_k_similar_queries(query_text, collection):
    # query_text = "How many white Nike tshirts are left in extra small size?"
    results = collection.query(
        query_texts=[query_text],
        n_results=2,
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )  
    return results['metadatas'][0]

def get_llm_query(examples, llm, db, query_text):
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=pt.example_prompt,
        prefix=pt.mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
    )

    new_chain = create_sql_query_chain(llm=llm, db=db, prompt=few_shot_prompt)

    query = new_chain.invoke(
        {
            "question": query_text
        }
    )
    return query

