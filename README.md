# Intelligent Talent Acquisition Assistant using Agentic AI

A B.Tech 6th Semester Generative AI Project

## Team Delta

## Project Overview
An intelligent HR recruitment system powered by multiple AI agents that automates
the entire talent acquisition pipeline from sourcing to scheduling.

## Tech Stack
- Python + Streamlit
- CrewAI (Multi-Agent Framework)
- LangChain (Prompt Engineering)
- HuggingFace (Mistral-7B LLM + Embeddings)
- ChromaDB (Vector Database)

## Features
- AI Agent Network (Sourcing, Screening, Engagement, Scheduling)
- 100 Candidate Database with Semantic Search
- HR Manager Chatbot powered by HuggingFace AI
- Real-time Analytics Dashboard
- Auto Email Generation and Interview Scheduling

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Add HuggingFace API key to `.env` file
3. Run: `streamlit run app.py`

## Project Structure
- `app.py` - Main Streamlit UI
- `vector_db.py` - Candidate database + ChromaDB
- `crew_setup.py` - HuggingFace LLM + CrewAI pipeline
- `agents.py` - CrewAI agent definitions
- `tasks.py` - CrewAI task definitions
- `resume_loader.py` - Scoring and helper functions
```

**Step 8:** Press **Ctrl + S** to save

---

### Method 2 — Using Notepad

**Step 1:** Open your project folder in File Explorer

**Step 2:** Right click on empty space inside the folder

**Step 3:** Click **New** → **Text Document**

**Step 4:** A new file appears — **before pressing anything else** rename it to exactly:
```
README.md