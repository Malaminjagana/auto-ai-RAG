from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
from rag.retriever import retrieve_knowledge
import os
import time

# LOAD ENVIRONMENT VARIABLES

load_dotenv()


# CREATE FASTAPI APP

app = FastAPI()
# CORS
# LOCAL DEVELOPMENT ONLY


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://malamin-profile.vercel.app",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        # "http://127.0.0.1:5500",
        # "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# GEMINI CLIENT


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
        "message": "Malamin AI RAG  is running!"
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
        # START TIMER
        
        retrieval_start = time.perf_counter()
        institute_knowledge = retrieve_knowledge(user_message)
        retrieval_time = time.perf_counter() - retrieval_start

        print(f"RAG retrieval time: {retrieval_time:.2f} seconds")










        # -------------------------------------------------
        # STEP 1: SEARCH THE KNOWLEDGE BASE
        # -------------------------------------------------

        institute_knowledge = retrieve_knowledge(
            user_message
        )


        # -------------------------------------------------
        # STEP 2: SEND KNOWLEDGE + QUESTION TO GEMINI
        # -------------------------------------------------

        interaction = client.interactions.create(

            model="gemini-3.7-flash",

            input=f"""
You are the professional AI assistant for Malamin Jagana.

Your job is to answer questions about Malamin Jagana's
professional background, skills, experience, education,
projects, certifications, languages, and other information
contained in the knowledge base.

IMPORTANT RULES:

1. Use the retrieved knowledge as your factual source.

2. Answer the user's question directly and naturally.

3. Do NOT say:
   - "Based on the provided information..."
   - "According to the provided information..."
   - "According to the knowledge base..."
   - "The retrieved information says..."
   - "The context states..."
   - "From the provided context..."

4. Do not mention the RAG system, knowledge base, chunks,
   retrieved information, context, or AI instructions.

5. Do not invent or guess information.

6. If the answer is clearly available in the retrieved
   knowledge, give the answer directly.

7. If the retrieved knowledge does not contain the answer,
   say:
   "I don't have that information."

8. If the question asks for a specific fact, answer with
   the specific fact first.

9. Keep answers professional, natural, concise, and
   useful to recruiters or potential clients.

10. When appropriate, provide a short explanation or
    relevant additional details, but do not unnecessarily
    repeat information.

RETRIEVED MALAMIN KNOWLEDGE:
{institute_knowledge}

USER QUESTION:
{user_message}

ANSWER:
"""
        )


        # -------------------------------------------------
        # STEP 3: GET GEMINI'S ANSWER
        # -------------------------------------------------

        answer = interaction.output_text


    
        # STEP 4: SEND ANSWER BACK TO WEBSITE
       

        return ChatResponse(
            answer=answer
        )


    except Exception as error:

        # -------------------------------------------------
        # ERROR HANDLING
        # -------------------------------------------------

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