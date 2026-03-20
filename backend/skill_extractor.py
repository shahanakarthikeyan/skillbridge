import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("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"))

def extract_skills(text, source):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=1500,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a skill extraction engine. Return ONLY valid JSON, no markdown, no explanation."
                },
                {
                    "role": "user",
                    "content": f"""Extract skills from this {source} text.

Text: {text[:3000]}

Return this exact JSON format:
{{"skills": [{{"name": "python", "level": "beginner", "years": 2, "category": "Programming"}}], "trace": "found X skills"}}

level must be: beginner, intermediate, or advanced
category must be: Programming, Data, Cloud, Management, Communication, Domain-specific"""
                }
            ]
        )

        raw = response.choices[0].message.content.strip()
        print(f"Raw response for {source}: {raw[:200]}")

        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        data = json.loads(raw.strip())
        skills = data.get("skills", [])
        print(f"Extracted {len(skills)} skills from {source}")

        trace = [{
            "step": f"Skill extraction ({source})",
            "reasoning": data.get("trace", ""),
            "output_count": len(skills)
        }]

        return skills, trace

    except Exception as e:
        print(f"Extraction error for {source}: {str(e)}")
        return [], [{"step": "extraction", "reasoning": str(e), "output_count": 0}]