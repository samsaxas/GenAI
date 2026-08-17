from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
import os


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    api_key=os.environ['GEMINI_API_KEY'],
    temperature=0
)


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm | StrOutputParser()


store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)


user1 = chain_with_memory.invoke(
    {"input": "My name is Alice."},
    config={"configurable": {"session_id": "user_1"}}
)

print("User 1:", user1)


user1 = chain_with_memory.invoke(
    {"input": "What is my name?"},
    config={"configurable": {"session_id": "user_1"}}
)

print("User 1:", user1)


user2 = chain_with_memory.invoke(
    {"input": "What is my name?"},
    config={"configurable": {"session_id": "user_2"}}
)

print("User 2:", user2)


print("\nStored Sessions:")
print(store)