import os
import subprocess

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings

# loading .env
load_dotenv()

# Starting ollama environment
password = os.getenv("password")
subprocess.call(f"echo {password} "
                f"| sudo -S systemctl start ollama", shell=True)

chunk_size = 40
chunk_overlap = 10

quote = (
    "One machine can do the work of fifty ordinary humans. "
    "No machine can do the work of one extraordinary human."
)

# Defining splitter
ct_splitter = CharacterTextSplitter(
    separator=".", chunk_size=chunk_size, chunk_overlap=chunk_overlap
)

# Splitting quote using CharacterTextSplitter
docs = ct_splitter.split_text(quote)

# Defining the model
llm = Ollama(base_url="http://localhost:11434", model="llama2")

# Creating vector database with embeddings from docs
vectorstore = Chroma.from_texts(texts=docs,
                                embedding=OllamaEmbeddings(model="llama2")
                                )

# Converting the vector database to a retriever object
retriever = vectorstore.as_retriever()

# Prompt template
template = ("Use the following pieces of context to answer the question at"
            " the end. If you don’t know the answer, just say that you don’t"
            " know, don’t try to make up an answer. Use three sentences "
            "maximum and keep the answer as concise as possible. {context}"
            " Question: {question} Helpful Answer:")

QA_chain_prompt = PromptTemplate(
    input_variables=["context", "question"], template=template
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm, retriever=retriever, chain_type_kwargs={"prompt": QA_chain_prompt}
)

question = "How many machines can do my work?"
query = qa_chain.invoke({"query": question})
print(query["result"])
