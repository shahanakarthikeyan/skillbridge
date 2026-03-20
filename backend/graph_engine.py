import json, os

# Load course catalog
CATALOG_PATH = os.path.join(os.path.dirname(__file__), "course_catalog.json")
with open(CATALOG_PATH) as f:
    CATALOG = json.load(f)

def build_pathway(gap_result: dict) -> tuple[list, list]:
    gaps = gap_result["gaps"]
    pathway = []
    trace = []

    for gap in gaps:
        skill = gap["skill"]
        required_level = gap["required_level"]
        current_level = gap["current_level"]
        category = gap["category"]

        # Find matching courses from catalog
        matching = [
            c for c in CATALOG
            if skill.lower() in c["skills_covered"]
            and c["level"] == required_level
        ]

        if not matching:
            # Fallback: find by category
            matching = [
                c for c in CATALOG
                if c["category"] == category
                and c["level"] == required_level
            ]

        if matching:
            # A* heuristic: pick course with highest relevance score
            best = max(matching, key=lambda c: c.get("relevance_score", 0))
            pathway.append({
                "skill_gap": skill,
                "priority": gap["priority"],
                "course": best,
                "from_level": current_level,
                "to_level": required_level,
                "estimated_hours": best.get("hours", 10)
            })
            trace.append(
                f"Gap '{skill}': selected '{best['title']}' "
                f"(score={best.get('relevance_score',0)}) via A* heuristic"
            )
        else:
            trace.append(f"Gap '{skill}': no course found in catalog — skipped")

    # Sort pathway: high priority first
    pathway.sort(key=lambda x: (x["priority"] != "high", x["priority"] != "medium"))

    total_hours = sum(p["estimated_hours"] for p in pathway)
    trace.append(f"Total pathway: {len(pathway)} modules, ~{total_hours} hours estimated")

    return pathway, trace