from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


vector_store = Chroma(
    collection_name="constitution_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

query = "how should the president be elected?"
k = 3
fetch_k = 5 
results = vector_store.similarity_search(
    query=query,
    k=k,
)

print(f"Number of results: {len(results)}")
for i, result in enumerate(results):
    print(f"Result {i + 1}:")
    print(f"Content: {result.page_content[:500]}")
    print(f"Metadata: {result.metadata}")
    print("-" * 80)

result = vector_store.max_marginal_relevance_search(
    query=query,
    k=k,
    fetch_k=fetch_k,
)

print(f"Number of results: {len(result)}")
for i, res in enumerate(result):
    print(f"Result {i + 1}:")
    print(f"Content: {res.page_content[:500]}")
    print(f"Metadata: {res.metadata}")
    print("-" * 80)