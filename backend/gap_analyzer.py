def compute_gap(resume_skills: list, jd_skills: list) -> dict:
    resume_map = {}
    for s in resume_skills:
        if isinstance(s, dict):
            name = s.get("name", "").lower().strip()
            resume_map[name] = s
            # Add partial name too (e.g. "machine learning" -> "ml")
            words = name.split()
            if len(words) > 1:
                resume_map[words[0]] = s

    jd_map = {}
    for s in jd_skills:
        if isinstance(s, dict):
            name = s.get("name", "").lower().strip()
            jd_map[name] = s

    gaps = []
    matched = []
    trace_lines = []

    level_score = {"none": 0, "beginner": 1, "intermediate": 2, "advanced": 3}

    def find_match(skill_name):
        # Exact match
        if skill_name in resume_map:
            return resume_map[skill_name]
        # Partial match - check if skill_name is contained in any resume skill
        for rkey, rval in resume_map.items():
            if skill_name in rkey or rkey in skill_name:
                return rval
        return None

    for skill_name, jd_skill in jd_map.items():
        match = find_match(skill_name)

        if match:
            jd_level = level_score.get(jd_skill.get("level", "intermediate"), 2)
            r_level = level_score.get(match.get("level", "beginner"), 1)

            if r_level < jd_level:
                delta = jd_level - r_level
                gaps.append({
                    "skill": skill_name,
                    "current_level": match.get("level", "beginner"),
                    "required_level": jd_skill.get("level", "intermediate"),
                    "priority": "high" if delta >= 2 else "medium",
                    "category": jd_skill.get("category", "Programming"),
                    "delta": delta
                })
                trace_lines.append(f"'{skill_name}': has {match.get('level')} needs {jd_skill.get('level')} GAP")
            else:
                matched.append(skill_name)
                trace_lines.append(f"'{skill_name}': matched at {match.get('level')} OK")
        else:
            gaps.append({
                "skill": skill_name,
                "current_level": "none",
                "required_level": jd_skill.get("level", "intermediate"),
                "priority": "high",
                "category": jd_skill.get("category", "Programming"),
                "delta": level_score.get(jd_skill.get("level", "intermediate"), 2)
            })
            trace_lines.append(f"'{skill_name}': MISSING needs {jd_skill.get('level')}")

    gaps.sort(key=lambda x: (-x["delta"], x["priority"]))

    total = len(jd_map)
    coverage = round(len(matched) / max(total, 1) * 100, 1)

    return {
        "gaps": gaps,
        "matched": matched,
        "coverage_pct": coverage,
        "trace": trace_lines
    }