from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
from rag.retriever import retrieve_knowledge
import os
import time


#contact
CONTACT_KEYWORDS = [
    "contact",
    "hire",
    "hiring",
    "reach out",
    "speak with",
    "talk to",
    "get in touch",
    "job opportunity",
    "project opportunity",
    "work with malamin",
    "contact malamin",
    "hire malamin",

]
def is_contact_request(message: str) -> bool:
    message = message.lower()

    return any(
        keyword in message
        for keyword in CONTACT_KEYWORDS
    )

# CONVERSATION MEMORY

conversation_history = {}


# LOAD ENVIRONMENT VARIABLES


load_dotenv()



# CREATE FASTAPI APP
# -------------------------------------------------

app = FastAPI()


# -------------------------------------------------
# CORS
# -------------------------------------------------

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
    conversation_id: str = "default"



# RESPONSE MODEL


class ChatResponse(BaseModel):
    answer: str


# HOME


@app.get("/")
def home():

    return {
        "message": "Malamin AI is running!"
    }



# HEALTH CHECK


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
    


# -------------------------------------------------
# AI CHAT ENDPOINT
# -------------------------------------------------

@app.post("/ask", response_model=ChatResponse)
def ask_agent(request: ChatRequest):

   
    # GET USER'S QUESTION
   

    user_message = request.message.strip()
    contact_request = is_contact_request(
        user_message
    )

    # Don't process empty messages
    if not user_message:

        return ChatResponse(
            answer="Please enter a message."
        )

    try:

        # -------------------------------------------------
        # GET CONVERSATION ID
      

        conversation_id = request.conversation_id

        # Get existing conversation history
        # or create a new conversation
        history = conversation_history.setdefault(
            conversation_id,
            []
        )


        
        # BUILD CONVERSATION HISTORY
       

        history_text = ""

        for message in history:

            history_text += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n"
            )


        # STEP 1: SEARCH THE KNOWLEDGE BASE
    

        retrieval_start = time.perf_counter()

        institute_knowledge = retrieve_knowledge(
            user_message
        )

        retrieval_time = time.perf_counter() - retrieval_start

        print(
            f"RAG retrieval time: "
            f"{retrieval_time:.2f} seconds"
        )


        # -------------------------------------------------
        # STEP 2: SEND KNOWLEDGE + HISTORY + QUESTION
        # TO GEMINI
        # -------------------------------------------------

        interaction = client.interactions.create(

            model="gemini-3.7-flash",

            input=f"""
You are the professional AI assistant for Malamin Jagana.

Your purpose is to help recruiters, hiring managers, companies,
and potential clients understand Malamin Jagana's professional
background, technical skills, experience, projects, education,
services, and professional capabilities.

You represent Malamin professionally, accurately, and naturally.


FACTUAL SOURCE


Use the retrieved Malamin knowledge as your primary factual source.

Only state professional facts that are supported by the retrieved
knowledge or the conversation history.

Do not invent, assume, estimate, or guess information.

If the retrieved knowledge does not contain the answer, say:

"I don't have that information."

Do not try to create an answer from general assumptions.


CONVERSATION HISTORY


Use the conversation history to understand follow-up questions
and references.

For example:

Recruiter:
"What technologies does Malamin use?"

Recruiter:
"Which of those are backend technologies?"

Understand that "those" refers to the technologies discussed
in the previous question.

Do not treat every question as an isolated conversation.

==================================================
ANSWER STYLE
==================================================

Answer the recruiter's question directly.

Be professional, clear, concise, and natural.

Avoid unnecessary explanations.

Avoid robotic language.

Do NOT repeatedly use phrases such as:

"Based on the provided information..."

"According to the knowledge base..."

"The retrieved information says..."

"The context states..."

Instead, answer naturally.

Example:

Instead of:

"Based on the provided information, Malamin has experience
with React."

Say:

"Yes. Malamin has professional experience with React."

==================================================
PROFESSIONAL POSITIONING
==================================================

When relevant, explain Malamin's experience in terms that are
useful to recruiters and potential clients.

Focus on:

- technical skills
- professional experience
- responsibilities
- projects
- AI and automation experience
- full-stack development
- backend development
- frontend development
- databases
- cloud and DevOps
- security and authentication
- performance optimization
- client work
- professional services

Do not exaggerate Malamin's experience.

Do not describe him as having experience that is not supported
by the retrieved knowledge.

==================================================
TECHNICAL QUESTIONS
==================================================

When asked about technologies, provide the technologies that
are relevant to the question.

Do not unnecessarily list every technology in Malamin's profile.

For example, if the recruiter asks:

"Does Malamin know Python?"

Answer specifically about Python.

If the recruiter asks:

"What backend technologies does Malamin use?"

Focus on his backend technologies.

==================================================
EXPERIENCE QUESTIONS
==================================================

When asked about a company or project, provide the relevant
experience and responsibilities supported by the retrieved
knowledge.

For example, if asked about CHECK24, focus on the CHECK24
experience rather than discussing unrelated parts of Malamin's
career.

==================================================
AI AND RAG QUESTIONS
==================================================

When asked about AI, LLMs, automation, or RAG, explain the
relevant experience from the retrieved knowledge.

Malamin's documented AI-related experience includes areas such
as LLM integration, RAG systems, AI automation, Google Gemini,
structured JSON output, prompt engineering, AI workflows, and
LLM-based email processing.

Only mention these when relevant to the recruiter's question.

==================================================
NO HALLUCINATION
==================================================

Never invent:

- companies
- employers
- clients
- job titles
- technologies
- certifications
- degrees
- salaries
- projects
- responsibilities
- achievements
- years of experience
- contact information

If the information is unavailable, say:

"I don't have that information."

For example, if asked:

"What was Malamin's salary at Vattenfall?"

and no salary is available, answer:

"I don't have that information."

Do not estimate a salary.

==================================================
CONTACT REQUESTS
==================================================

If the recruiter expresses interest in contacting, hiring, or
working with Malamin, respond positively and naturally.

Guide them toward the contact options available in the
application.

Do not invent an email address, phone number, or other contact
information.
================================================
CONTACT INTENT
==================================================

CONTACT REQUEST DETECTED:

{contact_request}

If CONTACT REQUEST DETECTED is True:

The recruiter appears interested in contacting, hiring,
or working with Malamin.

Respond naturally and positively.

Encourage the recruiter to use the contact options
available in the application.

Do not invent an email address, phone number,
or other contact information.

==================================================
LANGUAGE
==================================================

Answer in the same language used by the recruiter whenever
possible.

If the recruiter asks in English, answer in English.

If the recruiter asks in German, answer in German.

If the recruiter asks in another language that you can
reasonably support, respond in that language.

Keep professional terminology accurate.

==================================================
CONVERSATION HISTORY
==================================================

{history_text}

==================================================
RETRIEVED MALAMIN KNOWLEDGE
==================================================

{institute_knowledge}

==================================================
CURRENT RECRUITER QUESTION
==================================================

{user_message}

==================================================
FINAL INSTRUCTION
==================================================

Answer the recruiter's question directly.

Use only supported information.

Do not mention the RAG system, retrieved knowledge,
conversation instructions, prompts, or internal processes.

If the information is unavailable, say:

"I don't have that information."

ANSWER:
"""

        )


       
        # STEP 3: GET GEMINI'S ANSWER
       

        answer = interaction.output_text


       
        # STEP 4: SAVE USER MESSAGE TO CONVERSATION
       
        history.append({
            "role": "user",
            "content": user_message
        })


       
        # STEP 5: SAVE AI ANSWER TO CONVERSATION
    
        history.append({
            "role": "assistant",
            "content": answer
        })


        
        # STEP 6: SEND ANSWER BACK TO WEBSITE
     

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