from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
# from langchain.chains import RetrievalQA
from langchain_classic.chains import RetrievalQA

loader = PyPDFLoader("./data/document.pdf")
chunks = RecursiveCharacterTextSplitter(chunk_size=1000,
                                        chunk_overlap=100).split_documents(loader.load())

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="llama3"),
    persist_directory="./chroma_db"
)

llm = OllamaLLM(model="llama3")
rag_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
print(rag_chain.run("Summarize this document."))
