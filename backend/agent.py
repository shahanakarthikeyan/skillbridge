import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("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"))

def run_agent(resume_text: str, jd_text: str):
    from skill_extractor import extract_skills
    from gap_analyzer import compute_gap
    from graph_engine import build_pathway

    reasoning_steps = []

    # Step 1: Extract resume skills
    reasoning_steps.append({"step": "Calling tool: extract_skills", "reasoning": "Extracting skills from resume"})
    resume_skills, resume_trace = extract_skills(resume_text, "resume")
    reasoning_steps.append({"step": "Tool result: extract_skills", "reasoning": f"Found {len(resume_skills)} skills from resume"})

    # Step 2: Extract JD skills
    reasoning_steps.append({"step": "Calling tool: extract_skills", "reasoning": "Extracting skills from job description"})
    jd_skills, jd_trace = extract_skills(jd_text, "jd")
    reasoning_steps.append({"step": "Tool result: extract_skills", "reasoning": f"Found {len(jd_skills)} skills from JD"})

    # Step 3: Compute gap
    reasoning_steps.append({"step": "Calling tool: compute_skill_gap", "reasoning": "Comparing resume vs JD skills"})
    gap_result = compute_gap(resume_skills, jd_skills)
    reasoning_steps.append({"step": "Tool result: compute_skill_gap", "reasoning": f"Found {len(gap_result['gaps'])} gaps, coverage {gap_result['coverage_pct']}%"})

    # Step 4: Build pathway
    reasoning_steps.append({"step": "Calling tool: build_learning_pathway", "reasoning": "Building personalized pathway"})
    pathway, path_trace = build_pathway(gap_result)
    reasoning_steps.append({"step": "Tool result: build_learning_pathway", "reasoning": f"Built {len(pathway)} modules, ~{sum(p['estimated_hours'] for p in pathway)}h total"})

    # Step 5: Agent reflection via LLM
    try:
        reflection = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=300,
            temperature=0,
            messages=[{
                "role": "user",
                "content": f"You are SkillBridge AI. Summarize this onboarding analysis in 2 sentences:\n- Resume skills: {[s['name'] for s in resume_skills]}\n- JD requires: {[s['name'] for s in jd_skills]}\n- Gaps found: {[g['skill'] for g in gap_result['gaps']]}\n- Pathway: {[p['course']['title'] for p in pathway]}"
            }]
        )
        agent_summary = reflection.choices[0].message.content
    except:
        agent_summary = f"Analyzed {len(resume_skills)} resume skills against {len(jd_skills)} job requirements. Found {len(gap_result['gaps'])} gaps with {len(pathway)} recommended courses."

    reasoning_steps.append({"step": "Agent conclusion", "reasoning": agent_summary})

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "skill_gap": gap_result,
        "pathway": pathway,
        "reasoning_trace": {
            "extraction": reasoning_steps[:4],
            "gap_analysis": reasoning_steps[4:6],
            "path_selection": reasoning_steps[6:]
        }
    }
