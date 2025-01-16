# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings


# to_vectorize = [
#     "How many tests have failed?",
#     "What is the test that took the most time?"
# ]

# few_shots = [
#     {"Question": "How many tests have failed?", "Answer": "312 tests failed."},
#     {"Question": "What is the test that took the most time?", "Answer": "Test ID 007 took the most time."}
# ]

# embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# vectorstore = Chroma.from_texts(to_vectorize, embedding=embeddings, metadatas=few_shots)
# query = "Which test had the highest time duration?"
# query_embedding = embeddings.embed_query(query)
# results = vectorstore.similarity_search(query_embedding, k=1)




import sqlite3
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData

# SQLite3 database path
sqlite_db_path = r'C:\Users\ARTHUR\fiverr project\parquet_database\database1.db'

# MySQL database credentials
db_user = "root"
db_password = "6877"
db_host = "localhost"
db_name = "machine_test"

# Connect to the SQLite3 database
sqlite_conn = sqlite3.connect(sqlite_db_path)
sqlite_cursor = sqlite_conn.cursor()

# Connect to the MySQL database
mysql_conn = pymysql.connect(user=db_user, password=db_password, host=db_host, database=db_name)
mysql_cursor = mysql_conn.cursor()

# Function to transfer data from SQLite to MySQL
def transfer_data():
    # Get all tables in SQLite
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()

    for table in tables:
        table_name = table[0]

        # Fetch data from SQLite
        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        data = sqlite_cursor.fetchall()

        # Get column names from SQLite
        sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
        columns = sqlite_cursor.fetchall()
        column_names = [column[1] for column in columns]

        # Create table in MySQL (if it doesn't exist)
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (" \
                           + ", ".join([f"{col[1]} {col[2]}" for col in columns]) + ");"
        mysql_cursor.execute(create_table_sql)

        # Insert data into MySQL
        insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['%s'] * len(column_names))})"
        mysql_cursor.executemany(insert_sql, data)
        mysql_conn.commit()

        print(f"Transferred table: {table_name}")

# Transfer all tables
transfer_data()

# Close connections
sqlite_conn.close()
mysql_conn.close()
