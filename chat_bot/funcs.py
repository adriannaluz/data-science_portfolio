from langchain_community.chat_models import ChatOllama

llm = ChatOllama(base_url="http://localhost:11434", model="llama2")


def sendPrompt(prompt):
    global llm
    response = llm.invoke(prompt)

    return response
