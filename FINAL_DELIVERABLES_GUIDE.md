# MindMapper AI — Finals Deliverables Guide

## What You Must Submit
- **Presentation Report Slides**: `.pptx` or `.pdf`
- **Public links**:
  - Streamlit app URL (recommended), and/or
  - Public GitHub repository URL

## Slide Deck Structure (Copy This)

### Slide 1 — Title
- Project: MindMapper AI
- Members: (list)
- Live demo URL:
- GitHub URL:

### Slide 2 — Objective
- Transition from a basic LLM wrapper → production-ready AI chatbot
- Add: retrieval/reasoning architecture + security defenses

### Slide 3 — Design Decisions (RAG vs Agentic AI)
- **Why RAG**: grounds answers on uploaded documents (external data)
- **Why Agentic AI**: planner chooses when to use tools (RAG / memory) vs normal chat
- **Why both**: better grounding + better use of history for more “app-like” behavior

### Slide 4 — Architecture (Diagram)
- Streamlit UI
- Prompt Defenses
- Planner (Agent)
- Tools:
  - Tool A: RAG retrieval over uploaded KB
  - Tool B: Session memory search over SQLite logs
- Groq LLM response generation

### Slide 5 — Models and Libraries
- **LLM (main)**: llama-3.3-70b-versatile (Groq)
- **LLM (planner/summary)**: llama3-8b-8192 (Groq)
- **Libraries**:
  - Streamlit (UI)
  - groq (LLM API)
  - PyPDF2 (PDF parsing)
  - sqlite3 (session persistence)
  - Optional: langfuse (prompt/version traces)

### Slide 6 — Prompt Engineering
- System prompt goals:
  - Empathy + journaling style
  - One question at a time
  - Crisis rule (988 only if self-harm mentioned)
- Planner prompt:
  - Outputs JSON: tool = rag / memory / none
- Prompt versioning:
  - Versions displayed in the UI
  - Optional Langfuse traces record prompt + output

### Slide 7 — Prompt Defenses & Security
- Injection scanning (user input + uploaded documents)
- Delimiter separation: `<user_input>...</user_input>`
- Untrusted context policy:
  - Document + memory are treated as data, not instructions
- No secret leakage (API keys stay in Secrets/.env)

### Slide 8 — Functional Demo (Live)
Demo in this order:
1. Normal conversation (empathetic + one question)
2. Upload PDF/TXT → ask a question “based on the upload” (RAG)
3. End & Save → ask about “previous sessions/patterns” (memory tool)
4. Attempt jailbreak (should refuse and redirect)

### Slide 9 — Links
- Streamlit URL
- GitHub URL

## How To Publish (Public Links)

### A) GitHub (Public)
1. Create a new public GitHub repo.
2. Push at minimum:
   - `app.py`
   - `requirements.txt`
   - `.gitignore`
3. Do **NOT** commit `.env`.

### B) Streamlit Community Cloud
1. Deploy from your GitHub repo.
2. Set main file: `app.py`
3. Add Streamlit Secrets:
   - `GROQ_API_KEY`
   - Optional Langfuse:
     - `LANGFUSE_PUBLIC_KEY`
     - `LANGFUSE_SECRET_KEY`
     - `LANGFUSE_HOST` (optional)
4. Deploy → copy the public URL.

## Demo Checklist (Fast)
- [ ] App opens with no errors
- [ ] RAG works with a PDF upload
- [ ] Memory tool works after at least one “End & Save”
- [ ] Prompt defenses block jailbreak attempts
- [ ] Slide deck contains links + architecture + prompts + demo steps

