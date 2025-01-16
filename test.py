from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


to_vectorize = [
    "How many tests have failed?",
    "What is the test that took the most time?"
]

few_shots = [
    {"Question": "How many tests have failed?", "Answer": "312 tests failed."},
    {"Question": "What is the test that took the most time?", "Answer": "Test ID 007 took the most time."}
]

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

vectorstore = Chroma.from_texts(to_vectorize, embedding=embeddings, metadatas=few_shots)
query = "Which test had the highest time duration?"
query_embedding = embeddings.embed_query(query)
results = vectorstore.similarity_search(query_embedding, k=1)