import os
import subprocess

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

llm = ChatOllama(base_url="http://localhost:11434", model="llama2")


def load_ollama():
    # loading .env
    load_dotenv()

    # Starting ollama environment
    password = os.getenv("password")
    subprocess.call(f"echo {password} "
                    f"| sudo -S systemctl start ollama", shell=True)


def create_vectordb(pdf_path: str):
    # Defining chunk attributes
    chunk_size = 500
    chunk_overlap = 100

    # Loading the pdf file
    pdf_loader = PyPDFLoader(pdf_path)
    pdf_data = pdf_loader.load()

    # Using CharacterTextSplitter to split sentences in chunks
    ct_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    docs = ct_splitter.split_documents(pdf_data)

    # Definig embedding model
    ollama_embeddings = OllamaEmbeddings(model="llama2")

    # Creating vector database with embedded chunks
    persist_path = (
        "/home/adrianna/Desktop/data-science_portfolio"
        "/chat_bot/vector_database"
    )
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=ollama_embeddings,
        persist_directory=persist_path
    )

    vectorstore.persist()

    print(f"Vector database saved on {persist_path}")


def run_llm_model():
    model = Ollama(base_url="http://localhost:11434", model="llama2")

    # path where the Chroma's vector database is saved
    persist_path = (
        "/home/adrianna/Desktop/data-science_portfolio"
        "/chat_bot/vector_database"
    )

    ollama_embeddings = OllamaEmbeddings(model="llama2")

    vectorstore = Chroma(
        persist_directory=persist_path, embedding_function=ollama_embeddings
    )
    vectorstore.get()

    # Converting the vector database to a retriever object
    retriever = vectorstore.as_retriever()

    # Prompt template
    template = (
        "Use the following pieces of context to answer the question at"
        " the end. If the question is in Spanish reply in Spanish, "
        "if not reply in English. If you don’t know the answer, just "
        "say that you don’t know, don’t try to make up an answer. Use "
        "three sentences maximum and keep the answer as concise as "
        "possible. {context} Question: {question} Helpful Answer:"
    )

    QA_chain_prompt = PromptTemplate(
        input_variables=["context", "question"], template=template
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_chain_prompt}
    )

    return qa_chain


def sendPrompt(prompt):
    qa_chain = run_llm_model()
    response = qa_chain.invoke({"query": prompt})

    return response

