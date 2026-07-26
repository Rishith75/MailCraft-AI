import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

response = llm.invoke([
    HumanMessage(content="Hello")
])

print(response.content)