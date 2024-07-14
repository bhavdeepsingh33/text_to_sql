import run_sql as rn

question_examples = ["How many t-shirts do we have left for Nike in XS size and white color?",
                     "How much is the total price of the inventory for all S-size t-shirts?",
                     "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?",
                     "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?",
                     "How many white color Levi's shirt I have?",
                     "all adidas small tshirt along with discount",
                     "all large black tshirts with discount",
                     "all red tshirts with discount",
                     "return nike black tshirts without discount",
                     "lowest priced vanhusen tshirt without discount"
                     ]
sql_examples = {
    "query1":"SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
    "query2":"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
    "query3":"""select sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
            (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
            group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
            """,
    "query4":"SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
    "query5":"SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
    "query6":"""SELECT t.t_shirt_id as t_shirt_id_t, t.brand as brand_t, t.color as color_t, t.size as size_t, t.price as price_t, 
            t.stock_quantity as stock_quantity_t, d.pct_discount as pct_discount_d
            FROM t_shirts t JOIN discounts d ON t.t_shirt_id = d.t_shirt_id WHERE t.brand = 'Adidas' AND t.size = 'S'
            """,
    "query7":"""
            SELECT t.t_shirt_id as t_shirt_id_t, t.brand as brand_t, t.color as color_t, t.size as size_t, t.price as price_t, 
            t.stock_quantity as stock_quantity_t, d.pct_discount as pct_discount_d
            FROM t_shirts t JOIN discounts d ON t.t_shirt_id = d.t_shirt_id WHERE t.color = 'Black' AND t.size = 'L'
            """,
    "query8":"""
            SELECT t.t_shirt_id as t_shirt_id_t, t.brand as brand_t, t.color as color_t, t.size as size_t, t.price as price_t, 
            t.stock_quantity as stock_quantity_t, d.pct_discount as pct_discount_d
            FROM t_shirts t JOIN discounts d ON t.t_shirt_id = d.t_shirt_id WHERE t.color = 'Red'
            """,
    "query9":"""
            SELECT t.t_shirt_id, t.brand, t.color, t.size, t.price, t.stock_quantity
            FROM t_shirts t LEFT JOIN discounts d ON t.t_shirt_id = d.t_shirt_id WHERE t.brand='Nike' AND t.color = 'Black' AND d.pct_discount IS NULL
            """,
    "query10":"""
            SELECT t.t_shirt_id, t.brand, t.color, t.size, t.price, t.stock_quantity
            FROM t_shirts t LEFT JOIN discounts d ON t.t_shirt_id = d.t_shirt_id WHERE t.brand='Van Huesen' AND d.pct_discount IS NULL ORDER BY t.price ASC LIMIT 1
            """
}


def run_example_queries(db_path, sql_examples):
    import os
    result = []
    # connection = rn.connect_to_database()
    for i in sql_examples.keys():
        try:
            print(f"Executing {i}")
            # rn.query_result("t_shirts.db", query)
            print("os.getcwd()")
            print(os.getcwd())
            out = rn.query_result(db_path, sql_examples[i])
            print("out\n",out)
        except Exception as e:
            print(f"Error while executing query: {sql_examples[i]}")
            print(e)
        else:    
            print("str(out.values)\n",out.values)
            # result.append(str(out.values[0][0]))
            result.append(str(out.values))

            
    print(result)
    return result

def create_few_shots_list(questions, sqls, results):
    few_shots = []
    for question, sql_example, result in zip(questions, sqls, results):
        shot = {'Question' : question,
            'SQLQuery' : sqls[sql_example],
            'SQLResult': "Result of the SQL query",
            'Answer' : f"{result}"}
        few_shots.append(shot)
    return few_shots


# def get_few_shots():
#     results = run_example_queries()
#     few_shots = create_few_shots_list(question_examples, sql_examples, results)
#     return few_shots

# def create_vectordb(to_vectorize, few_shots):
#     client = chromadb.HttpClient()
#     collection = client.get_or_create_collection("t_shirts_sql")

#     collection.upsert(
#         documents=to_vectorize, # we embed for you, or bring your own
#         metadatas=few_shots, # filter on arbitrary metadata!
#         ids=[f"doc{i+1}" for i in range(len(to_vectorize))], # must be unique for each doc 
#     )
