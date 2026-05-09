def build_reply(state, recommendations):

    parts = []

    # Skills
    if state["skills"]:
        skill_text = ", ".join(state["skills"])
        parts.append(f"{skill_text} role")

    # Seniority
    if state["seniority"]:
        parts.append(f"{state['seniority']} level")

    # Personality
    if state["personality"]:
        parts.append("behavioral and stakeholder-fit needs")

    summary = ", ".join(parts)

    return (
        f"Based on your needs for "
        f"{summary}, here are "
        f"{len(recommendations)} relevant "
        f"SHL assessments."
    )