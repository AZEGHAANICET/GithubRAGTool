from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from langchain_core.messages import HumanMessage,SystemMessage
llm  =  ChatOllama(model="llama3:latest")

file_memory = FileChatMessageHistory(file_path="chat_history_anicet.json")
prompt = ChatPromptTemplate.from_messages(
    [
SystemMessage(content="You are a nice chatbot having a conversation with a human."),
        MessagesPlaceholder(variable_name="chat_history_anicet"),
        ("human", "{question}")
    ]
)


memory = ConversationBufferMemory(memory_key="chat_history_anicet", return_messages=True, chat_memory=file_memory)
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
    verbose=True
)


while True:
    a = input("Enter your query please Anicet :\n >")
    res = conversation.invoke({"question": a})
    print("="*10)
    print(res["text"])
    print("="*10)