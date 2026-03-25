from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import traceback
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import pdfplumber
import io

load_dotenv()

app = FastAPI(title="SkillBridge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    resume_text: str
    jd_text: str

class EmailRequest(BaseModel):
    email: str
    name: str
    pathway: list
    coverage_pct: float

@app.get("/health")
def health():
    return {"status": "ok", "mode": "agentic"}

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        if file.filename.endswith(".pdf"):
            with pdfplumber.open(io.BytesIO(contents)) as pdf:
                text = "\n".join([
                    page.extract_text() or ""
                    for page in pdf.pages
                ])
        else:
            text = contents.decode("utf-8")
        return {"text": text, "filename": file.filename}
    except Exception as e:
        return {"error": str(e)}

@app.post("/analyze")
async def analyze(req: AnalysisRequest):
    try:
        from agent import run_agent
        result = run_agent(req.resume_text, req.jd_text)
        return result
    except Exception as e:
        error_detail = traceback.format_exc()
        print("ERROR:", error_detail)
        return {"error": str(e), "detail": error_detail}

@app.post("/send-roadmap")
async def send_roadmap(req: EmailRequest):
    try:
        gmail_user = os.environ.get("GMAIL_USER")
        gmail_pass = os.environ.get("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_pass:
            return {"error": "Gmail not configured in .env file"}

        rows = "".join([
            f"""<tr>
              <td style='padding:12px;border:1px solid #333;color:#e2e8f0'>{i+1}. {p['skill_gap']}</td>
              <td style='padding:12px;border:1px solid #333;color:#a5b4fc'>{p['course']['title']}</td>
              <td style='padding:12px;border:1px solid #333;color:#ef4444'>{p['priority']}</td>
              <td style='padding:12px;border:1px solid #333;color:#94a3b8'>{p['estimated_hours']}h</td>
            </tr>"""
            for i, p in enumerate(req.pathway)
        ])

        html = f"""
        <html>
        <body style='font-family:Arial;margin:0;background:#0f0f1a'>
          <div style='background:linear-gradient(135deg,#6366f1,#8b5cf6);padding:40px;text-align:center'>
            <h1 style='color:white;margin:0;font-size:32px'>SkillBridge</h1>
            <p style='color:rgba(255,255,255,0.8);margin:8px 0 0'>Your Personalized Learning Roadmap</p>
          </div>
          <div style='padding:32px;background:#0f0f1a'>
            <p style='color:#e2e8f0;font-size:18px'>
              Hi <strong style='color:#818cf8'>{req.name}</strong>,
            </p>
            <p style='color:#94a3b8'>Here is your AI-generated onboarding pathway:</p>
            <div style='display:flex;gap:16px;margin:24px 0'>
              <div style='flex:1;background:#1e1e2e;border-radius:12px;padding:16px;text-align:center;border:1px solid rgba(99,102,241,0.2)'>
                <div style='font-size:24px;font-weight:800;color:#818cf8'>{len(req.pathway)}</div>
                <div style='color:#64748b;font-size:12px;margin-top:4px'>Modules</div>
              </div>
              <div style='flex:1;background:#1e1e2e;border-radius:12px;padding:16px;text-align:center;border:1px solid rgba(99,102,241,0.2)'>
                <div style='font-size:24px;font-weight:800;color:#818cf8'>
                  {sum(p["estimated_hours"] for p in req.pathway)}h
                </div>
                <div style='color:#64748b;font-size:12px;margin-top:4px'>Total hours</div>
              </div>
              <div style='flex:1;background:#1e1e2e;border-radius:12px;padding:16px;text-align:center;border:1px solid rgba(99,102,241,0.2)'>
                <div style='font-size:24px;font-weight:800;color:#818cf8'>{req.coverage_pct}%</div>
                <div style='color:#64748b;font-size:12px;margin-top:4px'>Coverage</div>
              </div>
            </div>
            <table width='100%' cellpadding='0' cellspacing='0'
              style='border-collapse:collapse;margin-top:20px'>
              <tr style='background:#6366f1'>
                <th style='padding:14px;color:white;text-align:left'>Skill Gap</th>
                <th style='padding:14px;color:white;text-align:left'>Course</th>
                <th style='padding:14px;color:white;text-align:left'>Priority</th>
                <th style='padding:14px;color:white;text-align:left'>Hours</th>
              </tr>
              {rows}
            </table>
            <p style='color:#64748b;margin-top:24px;font-size:14px'>
              Coverage: {req.coverage_pct}% of required skills addressed
            </p>
          </div>
          <div style='text-align:center;padding:24px;color:#334155;font-size:12px'>
            Generated by SkillBridge AI - Adaptive Onboarding Engine
          </div>
        </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Your SkillBridge Learning Roadmap - {req.name}"
        msg["From"] = gmail_user
        msg["To"] = req.email
        msg.attach(MIMEText(html, "html"))

        clean_pass = gmail_pass.replace(" ", "")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, clean_pass)
            server.sendmail(gmail_user, req.email, msg.as_string())

        return {"status": "sent", "to": req.email}

    except Exception as e:
        print(f"Email error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
