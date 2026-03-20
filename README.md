# SkillBridge - AI Adaptive Onboarding Engine

An agentic AI-powered onboarding engine that analyzes resumes against job descriptions and builds personalized learning pathways.

## Features
- PDF resume upload and text extraction
- Agentic AI skill extraction using Groq (Llama 3)
- Skill gap analysis with priority scoring
- Personalized learning pathway generation
- Reasoning trace visualization
- Email roadmap to inbox via Gmail

## Tech Stack
- Backend: FastAPI + Python
- Frontend: React + Vite
- AI: Groq API (Llama 3.1)
- Email: Gmail SMTP
- Deployment: Render

## Setup

### Backend
cd backend
pip install -r requirements.txt

Create .env file:
GROQ_API_KEY=your-key
GMAIL_USER=your@gmail.com
GMAIL_APP_PASSWORD=your-app-password

uvicorn main:app --reload

### Frontend
cd frontend
npm install
npm run dev

## Architecture
Resume + JD → Agent → Skill Extraction → Gap Analysis → Learning Pathway → Email
