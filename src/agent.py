import os
from langchain import hub
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings

# Load .env from parent directory
load_dotenv()

# Create system prompt for the refine chain
system_prompt = hub.pull("rlm/rag-prompt-llama3")

# Set up ChromaDB Vector Store
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = Chroma(
    collection_name="constitution_collection",
    embedding_function=embedding_function,
    persist_directory="./chroma_langchain_db",
)
retriever = vector_store.as_retriever(search_type="mmr", k=2, fetch_k=5)

# Groq LLM
llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.1,
    max_tokens=500,
)

# Create RetrievalQA chain with refine logic using the custom prompt
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": system_prompt}
)

# Function to ask a question
def chat(question: str):
    response = qa_chain.invoke({"query": question})
    return response
