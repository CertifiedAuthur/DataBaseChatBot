from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain_community.llms import OpenAI
from few_shots import few_shots
from pydantic import BaseModel
import pymysql

def get_few_shot_db_chain(api_key: str):
    try:
        # Initialize OpenAI with the provided API key
        openai = OpenAI(api_key=api_key)
        print("OpenAI initialized with API key.")
    except Exception as e:
        print(f"Error initializing OpenAI API: {e}")
        return None
    
    # MySQL database credentials
    db_user = "root"
    db_password = "6877"
    db_host = "localhost"
    db_name = "machine_test"

    try:
        # Try connecting to MySQL database
        db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}", sample_rows_in_table_info=3)
        print("Database connected successfully")
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
    
    # Initialize embedding model
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    print("Embedding model defined")
    
    # Vectorize few shots (if defined elsewhere in the project)
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    print("Few shots vectorized")
    
    # Create vectorstore with embeddings
    vectorstore = Chroma.from_texts(to_vectorize, embedding=embeddings, metadatas=few_shots)
    print("Embeddings generated...")

    # Initialize example selector
    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)
    print(f"Example selector: {example_selector}")

    # Define the prompt template
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}"
    )

    # Define few-shot prompt
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=_mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"]
    )
    
    # Callbacks and model setup
    class Callbacks(BaseModel):
        pass

    class Model(BaseModel):
        a: Callbacks

    try:
        Model.model_rebuild()
        SQLDatabaseChain.model_rebuild()
        print("Model rebuild completed successfully.")
    except Exception as e:
        print(f"Error during model rebuild: {e}")
        return None

    # Return the final SQL database chain
    db_chain = SQLDatabaseChain.from_llm(openai, db, verbose=True, prompt=few_shot_prompt)
    return db_chain
