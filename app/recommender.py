import json

def load_catalog():
    with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
        catalog = json.load(f)
    return catalog

def recommend_assessments(state, catalog):

    recommendations = []

    for item in catalog:
        score = 0
        name = item.get("name", "").lower()
        description = item.get(
            "description",
            ""
        ).lower()
        text = name + " " + description
        keys = [
            key.lower()
            for key in item.get("keys", [])
        ]
        # -------------------------
        # TECHNICAL MATCH
        # -------------------------
        technical_match = False
        for skill in state["skills"]:
            if skill in text:
                score += 6
                technical_match = True
        # -------------------------
        # PERSONALITY MATCH
        # -------------------------
        if state["personality"]:
            personality_categories = [
                "personality & behavior",
                "competencies",
                "development & 360"
            ]
            for category in personality_categories:

                if category in keys:
                    score += 3
                    break

        # -------------------------
        # SENIORITY MATCH
        # -------------------------
        seniority = state.get("seniority")

        if seniority:

            job_levels = [
                level.lower()
                for level in item.get("job_levels", [])
            ]

            if seniority == "fresher":
                if ("entry-level" in job_levels or "graduate" in job_levels):
                    score += 2
            elif seniority == "mid":
                if "mid-professional" in job_levels:
                    score += 2
            elif seniority == "senior":
                if ("manager" in job_levels or "director" in job_levels):
                    score += 2

        # -------------------------
        # FILTER BAD MATCHES
        # -------------------------
        if state["skills"] and not technical_match:

            # Allow ONLY strong personality tests
            allowed_names = [
                "opq",
                "global skills",
                "personality"
            ]
            valid = False
            for keyword in allowed_names:
                if keyword in text:
                    valid = True
                    break
            if not valid:
                continue

        # -------------------------
        # FINAL ADD
        # -------------------------
        if score > 0:
            recommendations.append({
                "score": score,
                "name": item.get("name", "Unknown"),
                "url": item.get("link", ""),
                "test_type": ", ".join(item.get("keys", []))
            })

    recommendations.sort(key=lambda x: x["score"], reverse=True)

    # Keep top technical tests
    final_results = recommendations[:6]

    # --------------------------------
    # Add personality assessments
    # --------------------------------
    if state["personality"]:
        personality_results = []
        for item in catalog:
            text = (
                item.get("name", "") + " " +
                item.get("description", "")
            ).lower()
            keys = [key.lower() for key in item.get("keys", [])]
            personality_categories = [
                "personality & behavior",
                "competencies",
                "development & 360"
            ]
            valid = False
            for category in personality_categories:
                if category in keys:
                    valid = True
                    break
            # Avoid duplicate Java tests
            if valid and "java" not in text:
                personality_results.append({
                    "score": 5,
                    "name": item.get("name", "Unknown"),
                    "url": item.get("link", ""),
                    "test_type": ", ".join(item.get("keys", []))
                })

        # Add ONLY top 2 personality assessments
        final_results.extend(personality_results[:2])

    # --------------------------------
    # Remove Duplicates
    # --------------------------------
    unique_results = []

    seen_urls = set()

    for item in final_results:
        if item["url"] not in seen_urls:
            unique_results.append(item)
            seen_urls.add(item["url"])

    return unique_results[:10]