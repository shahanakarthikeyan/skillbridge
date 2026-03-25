import json
import os

CATALOG_PATH = os.path.join(os.path.dirname(__file__), "course_catalog.json")
with open(CATALOG_PATH) as f:
    CATALOG = json.load(f)

# Role-specific course preferences
ROLE_CATEGORY_PRIORITY = {
    "data": ["Data", "Programming", "Cloud"],
    "engineer": ["Programming", "Cloud", "Data"],
    "fullstack": ["Programming", "Cloud", "Data"],
    "frontend": ["Programming", "Design"],
    "backend": ["Programming", "Cloud"],
    "designer": ["Design", "Communication"],
    "uiux": ["Design", "Communication"],
    "marketing": ["Communication", "Management", "Data"],
    "manager": ["Management", "Communication"],
    "devops": ["Cloud", "Programming"],
}

def get_role_priorities(jd_skills):
    all_skills = " ".join([s.get("name", "").lower() for s in jd_skills if isinstance(s, dict)])
    
    if any(k in all_skills for k in ["figma", "ux", "ui", "wireframe", "design", "prototype"]):
        return ROLE_CATEGORY_PRIORITY["designer"]
    elif any(k in all_skills for k in ["react", "javascript", "frontend", "css"]):
        return ROLE_CATEGORY_PRIORITY["frontend"]
    elif any(k in all_skills for k in ["docker", "kubernetes", "devops", "ci/cd"]):
        return ROLE_CATEGORY_PRIORITY["devops"]
    elif any(k in all_skills for k in ["machine learning", "ml", "data science", "analytics"]):
        return ROLE_CATEGORY_PRIORITY["data"]
    elif any(k in all_skills for k in ["marketing", "social media", "content"]):
        return ROLE_CATEGORY_PRIORITY["marketing"]
    elif any(k in all_skills for k in ["management", "leadership", "scrum"]):
        return ROLE_CATEGORY_PRIORITY["manager"]
    else:
        return ["Programming", "Data", "Cloud", "Design", "Management", "Communication"]

def find_course_for_skill(skill_name, required_level, role_priorities, used_ids):
    skill_lower = skill_name.lower().strip()
    candidates = []

    for c in CATALOG:
        if c["id"] in used_ids:
            continue
        score = 0

        # Skill match scoring
        for covered in c["skills_covered"]:
            if skill_lower == covered:
                score += 10
            elif skill_lower in covered or covered in skill_lower:
                score += 5

        if score == 0:
            continue

        # Level match scoring
        if c["level"] == required_level:
            score += 3
        elif c["level"] == "beginner" and required_level == "intermediate":
            score += 1

        # Category priority scoring
        if c["category"] in role_priorities:
            score += (len(role_priorities) - role_priorities.index(c["category"])) * 2

        score += c.get("relevance_score", 0.5) * 2
        candidates.append((score, c))

    if candidates:
        candidates.sort(key=lambda x: -x[0])
        return candidates[0][1]

    # Fallback: category match
    for priority_cat in role_priorities:
        matches = [
            c for c in CATALOG
            if c["category"] == priority_cat
            and c["id"] not in used_ids
        ]
        if matches:
            return max(matches, key=lambda x: x.get("relevance_score", 0))

    return None

def build_pathway(gap_result: dict) -> tuple:
    from agent import client

    gaps = gap_result.get("gaps", [])
    jd_skills = gap_result.get("jd_skills", [])
    pathway = []
    trace = []
    used_course_ids = set()

    role_priorities = get_role_priorities(jd_skills if jd_skills else [
        {"name": g["skill"]} for g in gaps
    ])

    trace.append(f"Role detected — category priority: {role_priorities}")

    for gap in gaps:
        skill = gap["skill"]
        required_level = gap.get("required_level", "beginner")

        course = find_course_for_skill(
            skill, required_level, role_priorities, used_course_ids
        )

        if course:
            used_course_ids.add(course["id"])
            pathway.append({
                "skill_gap": skill,
                "priority": gap.get("priority", "medium"),
                "course": course,
                "from_level": gap.get("current_level", "none"),
                "to_level": required_level,
                "estimated_hours": course.get("hours", 10)
            })
            trace.append(f"Gap '{skill}': matched '{course['title']}' (category: {course['category']})")
        else:
            trace.append(f"Gap '{skill}': no course found")

    pathway.sort(key=lambda x: (x["priority"] != "high", x["priority"] != "medium"))

    total_hours = sum(p["estimated_hours"] for p in pathway)
    trace.append(f"Total: {len(pathway)} modules, ~{total_hours} hours")

    return pathway, trace
