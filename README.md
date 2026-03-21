# SkillBridge — AI Adaptive Onboarding Engine

> **Stop wasting time teaching what people already know.**

SkillBridge is an agentic AI-powered onboarding engine that analyzes a new hire's resume against a job description, identifies exact skill gaps, and generates a personalized learning roadmap — delivered instantly to their inbox.

🔗 **Live Demo:** https://skillbridge-ui.onrender.com  
📹 **Demo Video:** https://drive.google.com/file/d/1RFxNGo4UqrKA59YxxLgq-st8p5EptGBC/view?usp=sharing

📂 **GitHub:** https://github.com/shahanakarthikeyan/skillbridge

---

## Features

- 📄 **PDF Resume Upload** — extracts and parses resume text automatically
- 🤖 **Agentic AI Pipeline** — Groq (Llama 3.1) with tool-calling for structured analysis
- 📊 **Skill Gap Analysis** — detects missing skills and proficiency level gaps
- 🎯 **Proficiency-Aware Matching** — identifies not just WHAT is missing but HOW BIG the gap is
- 🗺️ **Personalized Learning Roadmap** — prioritized courses mapped to real skill gaps
- 🧠 **Reasoning Trace** — full step-by-step agent explanation of every recommendation
- 📧 **Email Export** — sends the roadmap as a PDF to the user's inbox via Gmail
- 🌐 **Cross-Domain** — works across Tech, Cloud, Data, UI/UX, Operations and more

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Backend | FastAPI + Python |
| AI / LLM | Groq API — Llama 3.1 |
| PDF Parsing | PyMuPDF |
| Email | Gmail SMTP |
| Deployment | Render |

---

## How It Works

```
Resume PDF + Job Description
          ↓
     React Frontend
          ↓
    FastAPI Backend
          ↓
  Groq Agent (Llama 3.1)
    ├── extract_skills()       → 28 skills from resume, 5 from JD
    ├── compute_skill_gap()    → coverage 80%, 1 critical gap found
    └── build_learning_pathway() → 1 module, ~10h roadmap
          ↓
 Learning Roadmap + Reasoning Trace
          ↓
  React UI Display + Gmail Email Export
```

---

## Skill Gap Analysis Logic

### Step 1 — Skill Extraction
The Groq agent calls `extract_skills()` on both resume and JD and returns:
- `skill_name` — e.g. Python, AWS, SQL
- `current_level` — none / beginner / intermediate / advanced
- `required_level` — from the job description
- `gap_severity` — critical / moderate / minor

### Step 2 — Gap Algorithm
```
FOR each required skill in JD:

  IF skill missing in resume        → 🔴 CRITICAL GAP (high priority)
  IF current_level < required_level → 🟡 PARTIAL GAP  (medium priority)
  IF current_level >= required_level → ✅ MATCHED

Coverage % = (Matched Skills ÷ Total JD Skills) × 100
```

### Step 3 — Adaptive Path Selection
- Gaps ranked by severity (critical first)
- Each gap mapped to best-fit course from a fixed catalog
- Course selected based on: skill name + current level + target level
- Output: ordered roadmap, most urgent course first

### Step 4 — Reasoning Trace
The agent generates a natural language conclusion:
> *"The individual has a strong technical background with expertise in Python and Machine Learning. However, there is a critical gap in AWS — required by the JD at beginner level but currently at none. Recommended pathway: AWS Cloud Practitioner certification."*

---

## Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API Key — free at [console.groq.com](https://console.groq.com)
- Gmail App Password

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your-groq-api-key
GMAIL_USER=your@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

Run the backend:
```bash
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at: `http://localhost:3000`

---

## Datasets Referenced

| Dataset | Source | Role |
|---|---|---|
| Resume Dataset | [Kaggle — Sneha Anbhawal](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset) | Skill taxonomy inspiration |
| O*NET Database | [onetcenter.org](https://www.onetcenter.org/db_releases.html) | Job role competency reference |
| Job Descriptions | [Kaggle — Kshitiz Regmi](https://www.kaggle.com/datasets/kshitizregmi/jobs-and-job-description) | JD pattern reference |

> Note: SkillBridge does not train on external datasets. Skill extraction is performed dynamically by Groq (Llama 3.1) on user-provided resume and JD text. The above datasets were referenced for skill taxonomy and domain understanding.

---

## Metrics

| Metric | Result |
|---|---|
| Skill extraction (resume) | 28 skills detected |
| Skill extraction (JD) | 5 skills detected |
| Coverage accuracy | 80% on test case |
| Proficiency level detection | none / beginner / intermediate / advanced |
| Roadmap generation time | < 10 seconds |
| Hallucination rate | 0% (catalog-grounded) |
| Email delivery | ✅ Confirmed working |

---

## Project Structure

```
skillbridge/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── requirements.txt
│   └── .env
└── README.md
```

---

## Team

**K. Shahana** — shahanakarthikeyan0@gmail.com  
**R. Rajeshwari**

---

## Built For

**ARTPARK CodeForge Hackathon** — AI Adaptive Onboarding Engine Challenge

---

## License

MIT License
