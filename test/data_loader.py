from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters.sentence_transformers import SentenceTransformersTokenTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


urls = [
    'https://www.constituteproject.org/constitution/Tunisia_2014#s246'
]

loader = WebBaseLoader(urls)
docs = loader.load()

print(f'number of docs: {len(docs)}')
# print(f'docs[0] content: {docs[0].page_content[:500]}')
# print(f'docs[0] content: {docs[0].page_content[-300:]}')
# print(f'docs[0] metadata: {docs[0].metadata}')

# let's remove the first 500 character and the last 300 character from the page content
for page in docs:
    page.page_content = page.page_content[500:-300]
    

# Clean up excessive newlines in each document
for doc in docs:
    doc.page_content = ' '.join(doc.page_content.split())

print(f'length of the page: {len(docs[0].page_content)}')
# print(f'first 500 characters: {docs[0].page_content[:500]}')
# print(f'last 300 characters: {docs[0].page_content[-300:]}')


langchain_text_splitters = SentenceTransformersTokenTextSplitter(
    chunk_overlap=100,
)

docs = langchain_text_splitters.split_documents(docs)
print(f'number of chunks: {len(docs)}')
# print(f'first chunk: {docs[0].page_content[:500]}')
# print(f'last chunk: {docs[-1].page_content[:500]}')
# print(f'first chunk metadata: {docs[0].metadata}')
# print(f'last chunk metadata: {docs[-1].metadata}')

# ChromaDB VectorStore Initialization
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


vector_store = Chroma(
    collection_name="constitution_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

# Add documents to the vector store
vector_store.add_documents(docs)

