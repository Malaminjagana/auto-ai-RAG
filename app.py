from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv
from rag import retrieve_knowledge 

# LOAD ENVIRONMENT VARIABLES

load_dotenv()


# CREATE FASTAPI APP


app = FastAPI()



# CORS

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


# OPENAI CLIENT

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
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
        "message": "My AI Agent API is running!"
    }


# HEALTH CHECK

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

# AI CHAT ENDPOINT

@app.post("/ask", response_model=ChatResponse)
def ask_agent(request: ChatRequest):

    # Get the user's question
    user_message = request.message.strip()

    # Don't process empty messages
    if not user_message:
        return ChatResponse(
            answer="Please enter a message."
        )

    try:

        # STEP 1: SEARCH INSTITUTE KNOWLEDGE

        institute_knowledge = retrieve_knowledge(
            user_message
        )


        # STEP 2: SEND QUESTION + KNOWLEDGE TO GEMINI

        interaction = client.interactions.create(

            model="gemini-3.7-flash",

            input=f"""
You are the AI assistant for
Al-Imam Malick Islamic Institute.

Your job is to help website visitors
by answering questions about the institute.

Use the institute information provided below
to answer the user's question.

INSTITUTE INFORMATION:
{institute_knowledge}

USER QUESTION:
{user_message}

Instructions:

- Answer clearly and professionally.
- Use the institute information when it is relevant.
- Do not invent information about the institute.
- If the information is not available, say that
  you do not have that information.
- Keep the answer helpful and easy to understand.
"""
        )


        # STEP 3: GET GEMINI'S ANSWER

        answer = interaction.output_text


        # STEP 4: SEND ANSWER BACK TO WEBSITE

        return ChatResponse(
            answer=answer
        )


    except Exception as error:

    
        # ERROR HANDLING

        print(
            "AI ERROR:",
            error
        )

        return ChatResponse(
            answer=(
                "Sorry, I am having trouble "
                "connecting to the AI service."
            )
        )