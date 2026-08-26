from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# CREATE FASTAPI APPLICATION


app = FastAPI(
    title="Auto GPT RAG API",
    description="Backend API for the website AI chatbot",
    version="1.0.0"
)



# CORS
 

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# REQUEST MODEL

class ChatRequest(BaseModel):

    message: str 


# RESPONSE MODEL


class ChatResponse(BaseModel):

    answer: str 



# HOME

@app.get("/")
def home():

    return {
        "message": "lj AI Agent API is running!"
    }


# HEALTH CHECK


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# CHAT ENDPOINT

@app.post("/ask", response_model=ChatResponse)
def ask_agent(request: ChatRequest):

    user_message = request.message.strip()


    # Prevent empty messages

    if not user_message:

        return ChatResponse(
            answer="Please enter a message."
        )


    # Temporary response.
    #
    # We will replace this with
    # the real AI agent later.

    answer = (
        f"lj received your message : "
        f"{user_message}. We are working on it and will get back to you soon!"
    )


    return ChatResponse(
        answer=answer
    )