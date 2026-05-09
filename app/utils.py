from app.extractor import extract_info

def build_state(messages):
    state = {
        "skills": [],
        "seniority": None,
        "personality": False
    }
    for msg in messages:
        if msg.role != "user":
            continue
        extracted = extract_info(msg.content)
        # -------------------------
        # Merge Skills
        # -------------------------
        for skill in extracted["skills"]:
            if skill not in state["skills"]:
                state["skills"].append(skill)

        # -------------------------
        # Update Seniority
        # -------------------------
        if extracted["seniority"]:
            state["seniority"] = extracted["seniority"]

        # -------------------------
        # Update Personality
        # -------------------------
        if extracted["personality"]:
            state["personality"] = True

    return state