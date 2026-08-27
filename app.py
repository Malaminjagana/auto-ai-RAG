from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv


# LOAD ENVIRONMENT VARIABLES

load_dotenv()


# CREATE FASTAPI APP


app = FastAPI()


# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# OPENAI CLIENT
# =========================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =========================================
# REQUEST MODEL
# =========================================

class ChatRequest(BaseModel):

    message: str


# =========================================
# RESPONSE MODEL
# =========================================

class ChatResponse(BaseModel):

    answer: str


# =========================================
# HOME
# =========================================

@app.get("/")
def home():

    return {
        "message": "My AI Agent API is running!"
    }


# =========================================
# HEALTH CHECK
# =========================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =========================================
# AI CHAT ENDPOINT
# =========================================

@app.post("/ask", response_model=ChatResponse)
def ask_agent(request: ChatRequest):

    user_message = request.message.strip()


    # Don't process empty messages

    if not user_message:

        return ChatResponse(
            answer="Please enter a message."
        )


    try:

        # SEND MESSAGE TO GEMINI AI
        interaction = client.interactions.create(
            model="gemini-3.7-flash",
            input=user_message,
        )


        
        # GET AI TEXT

        answer = interaction.output_text


        return ChatResponse(
            answer=answer
        )


    except Exception as error:

        print(
            "AI ERROR:",
            error
        )


        return ChatResponse(
            answer="Sorry, I am having trouble connecting to the AI service."
        )