# 🤖 Malamin AI RAG Powered Recruiter Assistant

> A production-oriented Retrieval-Augmented Generation (RAG) application that provides recruiters and potential clients with accurate, context-aware answers about **Malamin Jagana's professional background, technical skills, experience, projects, education, services, and AI expertise.**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-purple)](https://www.trychroma.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google)](https://ai.google.dev/)
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)](https://vercel.com/)
[![Render](https://img.shields.io/badge/Backend-Render-46E3B7)](https://render.com/)

---

## 📌 Overview

**Malamin AI** is an AI-powered recruiter assistant built around a Retrieval-Augmented Generation architecture.

Instead of relying only on an LLM's general knowledge, the application retrieves relevant information from a structured knowledge base containing Malamin Jagana's professional information and provides that context to the LLM before generating an answer.

This helps the assistant:

- Answer questions using verified profile information
- Reduce unsupported or hallucinated answers
- Handle recruiter follow-up questions
- Provide context-aware professional responses
- Explain technical skills and project experience
- Support recruiter contact requests
- Separate factual knowledge retrieval from language generation

The project was intentionally built **without LangChain initially** to understand the underlying RAG architecture and implement the core components manually.

---

# 🧠 Architecture

The current system follows this architecture:

```text
                    ┌─────────────────────────┐
                    │        Recruiter        │
                    │      / Potential Client │
                    └────────────┬────────────┘
                                 │
                                 │ Question
                                 ▼
                    ┌─────────────────────────┐
                    │     Frontend Chatbot    │
                    │      HTML / JavaScript  │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP POST /ask
                                 ▼
                    ┌─────────────────────────┐
                    │       FastAPI API       │
                    │                         │
                    │  Request Validation     │
                    │  Conversation Memory    │
                    │  Contact Intent         │
                    └────────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
          ┌──────────────────┐      ┌──────────────────┐
          │   RAG Retriever  │      │ Conversation     │
          │                  │      │ History         │
          └────────┬─────────┘      └────────┬─────────┘
                   │                         │
                   ▼                         │
          ┌──────────────────┐               │
          │     ChromaDB     │               │
          │  Vector Database  │               │
          └────────┬─────────┘               │
                   │                         │
                   ▼                         │
          ┌──────────────────┐               │
          │ Malamin Knowledge│               │
          │      Base        │               │
          └────────┬─────────┘               │
                   │                         │
                   └────────────┬────────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │    Google Gemini    │
                     │        LLM          │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Professional Answer │
                     └─────────────────────┘
```

---

# 🔎 What is RAG?

**RAG = Retrieval-Augmented Generation**

RAG combines information retrieval with LLM generation.

Instead of:

```text
User Question
      │
      ▼
     LLM
      │
      ▼
   Answer
```

this application uses:

```text
User Question
      │
      ▼
Retrieve relevant knowledge
      │
      ▼
Provide context to LLM
      │
      ▼
     LLM
      │
      ▼
Context-aware Answer
```

### Example

A recruiter asks:

> "Does Malamin have experience with RAG?"

The system:

```text
Question
   │
   ▼
Retriever
   │
   ▼
ChromaDB
   │
   ▼
Relevant Malamin knowledge
   │
   ▼
Gemini
   │
   ▼
"Yes. Malamin has experience building
RAG-based AI applications..."
```

The LLM is therefore not expected to invent Malamin's professional history.

---

# 🏗️ RAG Pipeline

The knowledge pipeline follows:

```text
                Source Documents
                       │
                       ▼
              Document Extraction
                       │
                       ▼
                   Chunking
                       │
                       ▼
                 Vectorization
                       │
                       ▼
                   ChromaDB
                       │
                       ▼
               Semantic Retrieval
                       │
                       ▼
                 Relevant Context
                       │
                       ▼
                    Gemini
                       │
                       ▼
                     Answer
```

---

# 📚 Knowledge Base

The knowledge base is designed around professional recruiter use cases.

It contains information such as:

- Professional profile
- Technical skills
- Full-stack development
- AI and LLM experience
- RAG experience
- AI automation
- Frontend technologies
- Backend technologies
- Database experience
- Cloud and DevOps
- Security and authentication
- Professional experience
- Climkit experience
- Freelance projects
- Education
- Certifications
- Languages
- Professional services
- Portfolio information

The knowledge base is intentionally separated from the application logic.

This allows the AI application to retrieve factual information without hard-coding every answer into the chatbot.

---

# 🧩 Core Components

## 1. Document Ingestion

The ingestion pipeline reads supported knowledge files and converts them into searchable chunks.

```text
knowledge/
    │
    ├── profile.txt
    ├── experience.pdf
    ├── projects.docx
    └── ...
            │
            ▼
        ingest.py
            │
            ▼
        Text chunks
            │
            ▼
        ChromaDB
```

---

## 2. Chunking

Large documents are divided into smaller sections before being stored.

The goal is to retrieve **relevant pieces of information rather than entire documents**.

Conceptually:

```text
Large Document
      │
      ├── Chunk 1
      ├── Chunk 2
      ├── Chunk 3
      ├── Chunk 4
      └── ...
```

Chunk size and overlap can be tuned depending on retrieval quality.

---

## 3. Vector Database

The project uses **ChromaDB** as the vector database.

It stores the knowledge chunks in a form that allows semantic similarity searches.

```text
Question
   │
   ▼
Semantic Search
   │
   ▼
Similar Knowledge Chunks
```

---

## 4. Retriever

The retriever searches the vector database and returns the most relevant knowledge.

Example:

```python
retrieve_knowledge(
    "What backend technologies does Malamin use?"
)
```

The retriever returns relevant information which is then passed into the LLM prompt.

---

# 🧠 LLM Layer

The application uses **Google Gemini** as the language model.

The LLM receives:

```text
Conversation History
        +
Retrieved Knowledge
        +
Current User Question
        ↓
      Gemini
        ↓
Professional Answer
```

The LLM is responsible for:

- Understanding the question
- Understanding conversational context
- Interpreting retrieved information
- Generating natural language
- Following response rules
- Avoiding unsupported claims

---

# 💬 Conversation Memory

The chatbot supports conversational context.

Example:

```text
Recruiter:
"What technologies does Malamin use?"

Assistant:
"Malamin works with React, Angular, .NET, Python..."

Recruiter:
"Which of those are backend technologies?"

Assistant:
".NET, C#, Node.js, Express.js, Python..."
```

The second question depends on the previous conversation.

The application therefore maintains conversation history using a `conversation_id`.

```text
conversation_id
       │
       ▼
Conversation History
       │
       ├── User message
       ├── Assistant response
       ├── User message
       └── Assistant response
```

> Current implementation uses in-memory conversation storage. Persistent storage can be introduced later with Redis, PostgreSQL, or another persistence layer.

---

# 🛡️ Hallucination Protection

One of the important goals of this project is preventing the assistant from inventing professional information.

For example:

### Recruiter

> "What was Malamin's salary at Vattenfall?"

If the knowledge base does not contain salary information:

```text
"I don't have that information."
```

The system is instructed not to:

- Guess salaries
- Invent employers
- Invent certifications
- Invent degrees
- Invent projects
- Invent clients
- Invent responsibilities
- Invent contact information

This is especially important for recruiter-facing AI applications.

---

# 📞 Recruiter Contact Workflow

The application also contains a recruiter contact workflow.

```text
Recruiter
    │
    ▼
"I'd like to hire Malamin."
    │
    ▼
Contact Intent Detection
    │
    ▼
Contact Form
    │
    ├── Name
    ├── Company
    ├── Email
    ├── Position / Project
    └── Message
            │
            ▼
       POST /contact
            │
            ▼
        FastAPI
```

The current implementation receives and logs the contact request.

A future version can connect this endpoint to an email provider, CRM, or lead-management system.

---

# 🧪 Testing

The project includes dedicated tests for recruiter-oriented questions.

Example test categories:

### Technical

```text
Does Malamin work with Python?
Does Malamin have experience with React?
Does Malamin work with .NET?
```

### AI / RAG

```text
Does Malamin have AI experience?
Can Malamin build a RAG system?
Does Malamin work with LLMs?
```

### Professional Experience

```text
Tell me about Malamin's CHECK24 experience.
What did Malamin do at Vattenfall?
```

### Hallucination Tests

```text
Did Malamin work for Google?
What was Malamin's salary at Vattenfall?
Is Malamin an AWS certified architect?
```

### Contact Intent

```text
I'd like to hire Malamin.
How can I contact Malamin?
I have a project I'd like to discuss.
```

Testing is not limited to whether the API responds.

The goal is to evaluate:

```text
Retrieval Quality
        +
Answer Accuracy
        +
Conversation Context
        +
Hallucination Resistance
        +
Contact Intent
```

---

# 🗂️ Project Structure

```text
auto-gpt-rag/
│
├── app.py
│
├── rag/
│   ├── __init__.py
│   ├── ingest.py
│   └── retriever.py
│
├── knowledge/
│   └── ...
│
├── test/
│   ├── recruiter_questions.py
│   ├── test_recruiter_rag.py
│   └── test_hallucination.py
│
├── chroma_db/
│   └── ...
│
├── .env
├── .gitignore
└── README.md
```

---

# 🔌 API

## `GET /`

Basic API status endpoint.

## `GET /health`

Health check.

Example:

```json
{
  "status": "healthy"
}
```

## `POST /ask`

Main AI endpoint.

Example request:

```json
{
  "message": "What technologies does Malamin use?",
  "conversation_id": "recruiter-001"
}
```

## `POST /contact`

Recruiter contact endpoint.

Example:

```json
{
  "name": "Recruiter",
  "company": "Example GmbH",
  "email": "recruiter@example.com",
  "position": "Senior AI Engineer",
  "message": "We would like to discuss an opportunity."
}
```

---

# 🚀 Deployment Architecture

The application is designed as a separated frontend/backend system.

```text
                   INTERNET
                       │
                       ▼
        ┌────────────────────────────┐
        │          Vercel            │
        │       Portfolio / UI       │
        └──────────────┬─────────────┘
                       │
                       │ HTTPS
                       ▼
        ┌────────────────────────────┐
        │          Render            │
        │        FastAPI API         │
        └──────────────┬─────────────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
        ChromaDB              Gemini
             │                   │
             └─────────┬─────────┘
                       ▼
                AI Recruiter
                  Response
```

---

# 🧠 RAG vs LLM Applications vs AI Agents

This project is also designed to demonstrate the difference between several important concepts in modern AI engineering.

```text
                         AI APPLICATION
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
          RAG Application               Agent Application
                │                             │
                ▼                             ▼
               LLM                       LLM + Tools
                │                             │
                └──────────────┬──────────────┘
                               │
                               ▼
                       LLM Application
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
            LangChain                    LangGraph
```

### LLM

The language model provides language understanding and generation.

```text
Question → LLM → Answer
```

### RAG

RAG gives the LLM access to external knowledge.

```text
Question
   ↓
Retrieve Knowledge
   ↓
LLM
   ↓
Answer
```

### AI Agent

An agent can use tools and decide what action to take.

```text
User Request
      ↓
     Agent
      ↓
 ┌────┼────────┐
 ↓    ↓        ↓
Search Database API
 ↓    ↓        ↓
 └────┼────────┘
      ↓
     LLM
      ↓
    Result
```

### LangChain

LangChain provides reusable components for building LLM applications, including workflows involving:

- LLMs
- prompts
- document loaders
- retrievers
- tools
- chains
- structured outputs
- agents

### LangGraph

LangGraph is designed for more complex, stateful workflows where an application may need:

- multiple steps
- decisions
- loops
- state
- retries
- tool execution
- human approval

---

# 🔬 Why This Project Was Built Without LangChain Initially

The first version intentionally implements the RAG pipeline directly.

Instead of immediately using a framework:

```text
LangChain Retriever
      ↓
LangChain Chain
      ↓
LLM
```

the project implements the underlying concepts manually:

```text
Document Loading
      ↓
Chunking
      ↓
ChromaDB
      ↓
Retriever
      ↓
Prompt Construction
      ↓
Gemini
      ↓
Response
```

This approach makes it possible to understand:

- What retrieval actually does
- How chunking affects retrieval
- How context reaches the LLM
- How conversation memory works
- Where hallucinations can occur
- How prompts influence generation
- Where an AI framework adds value

LangChain and LangGraph can then be introduced as **engineering abstractions on top of concepts already understood**.

---

# 🔮 Future Architecture

The recruiter assistant is intentionally kept focused.

A separate future project can explore an agentic architecture.

For example:

## Project 1 — Recruiter RAG Assistant

```text
Recruiter
    ↓
RAG
    ↓
Malamin Knowledge
    ↓
Gemini
    ↓
Answer
```

## Project 2 — AI Job Search Agent

```text
                         AI JOB AGENT
                              │
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
          Job Search        RAG          Web Search
              │               │               │
              ↓               ↓               ↓
             Jobs             CV             Market
              └───────────────┼───────────────┘
                              ↓
                             LLM
                              ↓
                          Analysis
                              ↓
                     Application Generation
```

Potential technologies:

```text
LLM
 +
RAG
 +
Tools
 +
LangChain
 +
LangGraph
 =
Agentic AI Application
```

---

# 🎯 Engineering Goals

This project demonstrates practical understanding of:

- Retrieval-Augmented Generation
- Vector databases
- Semantic retrieval
- LLM integration
- Prompt engineering
- Conversation memory
- API design
- FastAPI
- Pydantic validation
- CORS
- AI hallucination protection
- AI application testing
- Contact intent detection
- Frontend/backend integration
- Deployment architecture
- Production-oriented AI engineering

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| LLM | Google Gemini |
| Vector Database | ChromaDB |
| Document Processing | PyPDF, python-docx |
| Validation | Pydantic |
| API | REST |
| Deployment | Vercel + Render |
| Version Control | Git + GitHub |

---

# ▶️ Local Development

Clone the repository:

```bash
git clone <https://github.com/Malaminjagana/auto-ai-RAG.git>
cd auto-gpt-rag
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

Build the knowledge base:

```bash
python3 rag/ingest.py
```

Start FastAPI:

```bash
uvicorn app:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Run retrieval tests:

```bash
python3 test/test_recruiter_rag.py
```

---

# 🔐 Security Notes

Secrets should never be committed to GitHub.

The `.env` file should remain local:

```text
.env
chroma_db/
.venv/
__pycache__/
```

The Gemini API key must be provided through environment variables.

---

# 📈 Current Status

### Implemented

- [x] Document ingestion
- [x] Document chunking
- [x] ChromaDB vector storage
- [x] Semantic retrieval
- [x] Gemini integration
- [x] FastAPI backend
- [x] Conversation memory
- [x] Recruiter-focused prompting
- [x] Hallucination testing
- [x] Contact intent detection
- [x] Recruiter contact endpoint
- [x] Frontend chatbot integration
- [x] Production deployment architecture
- [x] Retrieval performance measurement

### Planned Improvements

- [ ] Persistent conversation storage
- [ ] Advanced retrieval / reranking
- [ ] Automated evaluation metrics
- [ ] Rate limiting
- [ ] Production monitoring
- [ ] Real email/CRM integration
- [ ] LangChain implementation for comparison
- [ ] LangGraph agent project
- [ ] Tool-enabled AI agent

---

# 👨‍💻 About

**Malamin Jagana**

Senior Full-Stack Developer & AI Engineer

Specializing in:

- Full-Stack Web Development
- AI Integration
- RAG Systems
- LLM Applications
- AI Automation
- Backend Development
- Frontend Development
- API Development
- Cloud & DevOps
- WordPress

Portfolio:

**https://malamin-profile.vercel.app**

---

# 📚 Learning Architecture

The project follows a deliberate progression:

```text
                    AI ENGINEERING LEARNING PATH
                               │
                               ▼
                         Python / APIs
                               │
                               ▼
                              LLM
                               │
                               ▼
                              RAG
                               │
                               ▼
                     Retrieval Optimization
                               │
                               ▼
                    LLM Application Design
                               │
                               ▼
                           LangChain
                               │
                               ▼
                            Tools
                               │
                               ▼
                            Agents
                               │
                               ▼
                          LangGraph
                               │
                               ▼
                    Advanced Agent Systems
```

The objective is not simply to use AI frameworks, but to understand the architecture underneath them.

---

## ⭐ Key Takeaway

This repository demonstrates a progression from **manually implemented RAG fundamentals** toward more advanced **LLM application and agent architectures**.

```text
LLM
 │
 ├── RAG
 │    └── External Knowledge
 │
 ├── Tools
 │    └── External Capabilities
 │
 └── Agents
      └── Reason + Decide + Act

Frameworks:
LangChain → LLM application building blocks
LangGraph → Stateful agent workflows
```

> **The goal is to understand the system first, then use frameworks to make it more scalable, maintainable, and powerful.**
