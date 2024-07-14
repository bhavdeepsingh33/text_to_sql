import sqlite3
import pandas as pd

# def connect_to_database(db_path):
#     try:
#         # Connect to the database
#         connection = sqlite3.connect(f"{db_path}")
#     except:
#          print("connnection error")
#     return connection

def preprocess_query(query):
    query = query.replace("```", "")
    query = query.replace("sql", "")
    query = query.replace("\n", " ")
    return query

def query_result(db_path, query):
    from contextlib import closing
    with closing(sqlite3.connect(f"{db_path}")) as connection:
        with closing(connection.cursor()) as cursor:
            # Read a single record
            # sql = "SELECT * FROM t_shirts"
            cursor.execute(query)

            # Connection is not autocommit by default, so we must commit to save changes
            connection.commit()
            # Fetch all the records from SQL query output
            results = cursor.fetchall()
            # print(results)
            column_headers = [description[0] for description in cursor.description]
            
            # print(results)
            # Convert results into pandas dataframe
            df = pd.DataFrame(results, columns=column_headers)
            # print(df)
            # print(f'Successfully retrieved records')
            return df