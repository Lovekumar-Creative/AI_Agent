def extract_info(text):

    text = text.lower()

    info = {
        "skills": [],
        "seniority": None,
        "personality": False
    }

    # -------------------------
    # Skills
    # -------------------------
    skill_keywords = [
        "java",
        "python",
        "javascript",
        "sql",
        "backend",
        "frontend"
    ]

    for skill in skill_keywords:
        if skill in text:
            info["skills"].append(skill)

    # -------------------------
    # Seniority
    # -------------------------
    if ("fresher" in text or "entry" in text or "graduate" in text):
        info["seniority"] = "fresher"
    elif ("mid" in text or "4 years" in text or "5 years" in text):
        info["seniority"] = "mid"
    elif ("senior" in text or "lead" in text or "manager" in text):
        info["seniority"] = "senior"

    # -------------------------
    # Personality Detection
    # -------------------------
    personality_words = [
        "communication",
        "stakeholder",
        "personality",
        "behavior",
        "leadership",
        "teamwork",
        "collaboration"
    ]

    for word in personality_words:
        if word in text:
            info["personality"] = True
            
    return info