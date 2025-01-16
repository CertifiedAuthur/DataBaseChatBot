import streamlit as st
from langchain_helper import get_few_shot_db_chain

# Initialize session state for the question and answer
if "question" not in st.session_state:
    st.session_state["question"] = ""
if "answer" not in st.session_state:
    st.session_state["answer"] = ""

# Title of the Streamlit app
st.title("Database Q&A Chatbot")

# Prompt the user to paste their API key
api_key = st.sidebar.text_area("Paste your OpenAI API Key below:", height=150)

# Store the API key in session state once pasted
if api_key:
    st.session_state["OPENAI_API_KEY"] = api_key
    st.success("API Key has been set successfully!")

# Text input to capture the user's question
st.session_state["question"] = st.text_input("Enter your question:", value=st.session_state["question"])

# Button to trigger the chain execution
if st.button("Get Answer"):
    if "OPENAI_API_KEY" not in st.session_state:
        st.error("API Key not set. Please paste your API key to continue.")
    elif st.session_state["question"]:
        try:
            with st.spinner("Generating the answer..."):
                # Pass the API key to langchain_helper when calling get_few_shot_db_chain
                chain = get_few_shot_db_chain(api_key=st.session_state["OPENAI_API_KEY"])  # Pass the API key
                st.session_state["answer"] = chain.run(st.session_state["question"])  # Execute the chain
        except Exception as e:
            st.session_state["answer"] = f"An error occurred: {str(e)}"

# Display the answer if available
if st.session_state["answer"]:
    st.header("Answer:")
    st.write(st.session_state["answer"])
