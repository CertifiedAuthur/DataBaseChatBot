import streamlit as st
import sqlite3
import pandas as pd
import google.generativeai as genai

# Streamlit configuration
st.set_page_config(page_title="Text-to-SQL Application", layout="wide")
st.title("📊 Text-to-SQL with SQLite Database")

# Sidebar for Google API Key input
st.sidebar.header("Configuration")
google_api_key = st.sidebar.text_input("Enter your Google API Key", type="password")

# Check if the API key is provided
if google_api_key:
    try:
        # Configure the GenAI API
        genai.configure(api_key=google_api_key)
        st.sidebar.success("Google API Key configured successfully.")
    except Exception as e:
        st.sidebar.error(f"Failed to configure API Key: {str(e)}")

# Database connection
DATABASE_PATH = "database.db"
conn = sqlite3.connect(DATABASE_PATH)

# Extract schema from the database
def get_database_schema(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        schema[table_name] = column_names

    return schema

# Generate the prompt including the schema
def generate_prompt_with_schema(schema, query):
    schema_str = "\n".join([f"Table: {table}\nColumns: {', '.join(columns)}" for table, columns in schema.items()])
    prompt = f"""
    You are an SQL expert tasked with translating natural language questions into SQL queries for the following database schema:

    {schema_str}

    Query: {query}
    Provide the SQL query and explain the answer clearly.
    """
    return prompt

# Function to execute SQL query
def execute_query(sql_query):
    try:
        df = pd.read_sql_query(sql_query, conn)
        return df
    except Exception as e:
        return f"Error: {str(e)}"

# Function to extract SQL query from the AI response
def get_sql_query_from_response(response):
    try:
        # Extract the query (assumes SQL starts with 'SELECT')
        query_start = response.lower().find("select")
        query_end = response.rfind(";") + 1  # Include the semicolon
        sql_query = response[query_start:query_end]
        
        # Remove backticks and unwanted formatting
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        return sql_query
    except ValueError:
        st.error("Could not extract SQL query from the response.")
        return None


# Input section for user query
st.subheader("Ask Your Question")
user_query = st.text_input("Enter your question (e.g., How many tests failed?):")

generate_button = st.button("Generate Answer")

if generate_button and google_api_key and user_query:
    schema = get_database_schema(conn)
    prompt = generate_prompt_with_schema(schema, user_query)

    try:
        # Step 2: Generate SQL query using Google GenAI
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content([prompt])
        
        # Extract and sanitize SQL query
        sql_query = get_sql_query_from_response(response.text)
        
        if sql_query:
            st.subheader("Generated SQL Query")
            st.code(sql_query, language="sql")

            # Step 3: Execute SQL query and show results
            query_result = execute_query(sql_query)
            if isinstance(query_result, pd.DataFrame):
                st.subheader("Query Results")
                st.dataframe(query_result)

                # Add download button for results
                csv = query_result.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="query_results.csv",
                    mime="text/csv"
                )
            else:
                st.error(query_result)
        else:
            st.error("No valid SQL query was generated.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Close the database connection
conn.close()
