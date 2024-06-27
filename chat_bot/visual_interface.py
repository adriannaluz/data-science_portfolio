import streamlit as st

from funcs import sendPrompt

# Title of my app
st.title("Chat with Ollama")

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
            response = sendPrompt(prompt)
            print(response)
            st.write(response.content)  # Display only the content of the response
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)