import os
import time
import numpy as np
import streamlit as st

from chatbot_funcs import sendPrompt, run_llm_model, create_vectordb, load_ollama

if __name__ == '__main__':
    # Starting ollama environment
    # st.write("Loading the llm model")
    # load_ollama()

    vector_database_path = np.array(os.listdir("vector_database"))

    ## Checking if Chroma vector database exist
    if np.isin(vector_database_path, 'chroma.sqlite3').sum() == 0:
        print("Creating vector database with Chroma")
        start = time.time()

        pdf_path = "/home/adrianna/Desktop/neobank/chatbot/ollama/introduccion-a-las-finanzas-personales.pdf"
        llm_model = 'llama2'
        create_vectordb(pdf_path, llm_model)

        end = time.time()

        print(end - start)

    # Title of my app
    st.title('Financial SOS')
    st.markdown("##### HI, I'm your financial helper and I'm here to give you some "
                "best practice to make better use of your money =D")

    # Defining messages
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question!"}
        ]
    # Creating chat input box
    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message["content"])

    if st.session_state.messages[-1]['role'] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = sendPrompt(prompt) # ["result"]
                st.write(response["result"])  # Display only the content of the response
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)