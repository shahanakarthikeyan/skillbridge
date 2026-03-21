import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_skills(text, source):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=800,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "Extract skills and return ONLY JSON. No markdown."
                },
                {
                    "role": "user",
                    "content": "Extract skills from this " + source + ":\n\n" + text[:1500] + "\n\nReturn ONLY this JSON:\n{\"skills\": [{\"name\": \"python\", \"level\": \"beginner\", \"years\": null, \"category\": \"Programming\"}], \"trace\": \"found X skills\"}"
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
            "step": "Skill extraction (" + source + ")",
            "reasoning": data.get("trace", ""),
            "output_count": len(skills)
        }]

        return skills, trace

    except Exception as e:
        print(f"Extraction error for {source}: {str(e)}")
        return [], [{"step": "extraction", "reasoning": str(e), "output_count": 0}]
