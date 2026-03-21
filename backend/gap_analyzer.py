def compute_gap(resume_skills: list, jd_skills: list) -> dict:
    resume_map = {}
    for s in resume_skills:
        if isinstance(s, dict):
            name = s.get("name", "").lower().strip()
            resume_map[name] = s
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

    def get_gap_severity(delta):
        if delta >= 3:
            return "critical"
        elif delta >= 2:
            return "critical"
        elif delta == 1:
            return "moderate"
        else:
            return "minor"

    def get_progress(current, required):
        scores = {"none": 0, "beginner": 1, "intermediate": 2, "advanced": 3}
        current_score = scores.get(current, 0)
        required_score = scores.get(required, 3)
        if required_score == 0:
            return 100
        return round((current_score / required_score) * 100)

    def find_match(skill_name):
        if skill_name in resume_map:
            return resume_map[skill_name]
        for rkey, rval in resume_map.items():
            if skill_name in rkey or rkey in skill_name:
                return rval
        return None

    for skill_name, jd_skill in jd_map.items():
        match = find_match(skill_name)
        required_level = jd_skill.get("level", "intermediate")

        if match:
            current_level = match.get("level", "beginner")
            jd_level = level_score.get(required_level, 2)
            r_level = level_score.get(current_level, 1)

            if r_level < jd_level:
                delta = jd_level - r_level
                severity = get_gap_severity(delta)
                progress = get_progress(current_level, required_level)
                gaps.append({
                    "skill": skill_name,
                    "current_level": current_level,
                    "required_level": required_level,
                    "priority": "high" if delta >= 2 else "medium",
                    "category": jd_skill.get("category", "Programming"),
                    "delta": delta,
                    "gap_severity": severity,
                    "progress": progress
                })
                trace_lines.append(f"'{skill_name}': {current_level} → {required_level} ({severity} gap)")
            else:
                progress = 100
                matched.append({
                    "skill": skill_name,
                    "current_level": current_level,
                    "required_level": required_level,
                    "gap_severity": "none",
                    "progress": progress
                })
                trace_lines.append(f"'{skill_name}': matched at {current_level} ✅")
        else:
            severity = "critical"
            gaps.append({
                "skill": skill_name,
                "current_level": "none",
                "required_level": required_level,
                "priority": "high",
                "category": jd_skill.get("category", "Programming"),
                "delta": level_score.get(required_level, 2),
                "gap_severity": severity,
                "progress": 0
            })
            trace_lines.append(f"'{skill_name}': MISSING → {required_level} (critical gap)")

    gaps.sort(key=lambda x: (-x["delta"], x["gap_severity"]))

    total = len(jd_map)
    coverage = round(len(matched) / max(total, 1) * 100, 1)

    return {
        "gaps": gaps,
        "matched": matched,
        "coverage_pct": coverage,
        "trace": trace_lines
    }
