from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from langchain_community.chat_models import ChatOpenAI
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from typing import AsyncGenerator
from fastapi.responses import StreamingResponse
import os

# Set up API Key
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"

app = FastAPI()

# Allow all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend's domain in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Initialize LLM
llm = ChatOpenAI(model_name="codellama:13b-instruct", streaming=True)

# Streaming generator function
async def stream_chat_response(message: str) -> AsyncGenerator[str, None]:
    async for chunk in llm.astream([HumanMessage(content=message)]):
        yield chunk.content

# FastAPI endpoint for streaming response
@app.get("/chat")
async def chat_stream(message: str):
    return StreamingResponse(stream_chat_response(message), media_type="text/event-stream")

