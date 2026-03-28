import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# BÍ KÍP NẰM Ở ĐÂY: Sử dụng thế hệ model mới nhất
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite", 
    temperature=0, 
    google_api_key=os.getenv("GEMINI_API_KEY")
)