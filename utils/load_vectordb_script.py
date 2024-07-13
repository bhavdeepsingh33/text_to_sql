import few_shots as fs
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
import os

db_path = str(os.getcwd())+"/text_to_sql_deployed/t_shirts.db"
results = fs.run_example_queries(db_path, fs.sql_examples)

few_shots = fs.create_few_shots_list(fs.question_examples, fs.sql_examples, results)
print(few_shots)

to_vectorize = [" ".join(example.values()) for example in few_shots]
curr_dir = os.getcwd()
# client = chromadb.HttpClient()
client = chromadb.PersistentClient(
    path=curr_dir+"/text_to_sql_deployed/chromadb",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

# client.delete_collection(name="t_shirts_sql")

collection = client.get_or_create_collection("t_shirts_sql")

collection.upsert(
    documents=to_vectorize, # we embed for you, or bring your own
    metadatas=few_shots, # filter on arbitrary metadata!
    ids=[f"doc{i+1}" for i in range(len(to_vectorize))], # must be unique for each doc 
)