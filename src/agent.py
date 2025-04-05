import os
from langchain import hub
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate

# Load .env from parent directory
load_dotenv()

# Pull the original prompt
base_prompt = hub.pull("rlm/rag-prompt-llama3")

# Add your custom instruction
custom_instruction = (
    "You are a helpful assistant specialized in the Tunisian Constitution. "
)

modified_prompt = ChatPromptTemplate.from_messages(
        [("system", custom_instruction)] + base_prompt.messages
    )


# Set up ChromaDB Vector Store
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = Chroma(
    collection_name="constitution_collection",
    embedding_function=embedding_function,
    persist_directory="./chroma_langchain_db",
)
retriever = vector_store.as_retriever(
        search_kwargs={'k': 5}
)

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
    chain_type_kwargs={"prompt": modified_prompt}
)

# Function to ask a question
def chat(question: str):
    response = qa_chain.invoke({"query": question})
    return response
