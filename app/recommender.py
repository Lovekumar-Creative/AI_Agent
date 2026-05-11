import json

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------
# Load Embedding Model
# --------------------------------
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

catalog_embeddings = []

# --------------------------------
# Load Catalog
# --------------------------------
def load_catalog():

    global catalog_embeddings

    with open(
        "data/shl_catalog.json",
        "r",
        encoding="utf-8"
    ) as f:

        catalog = json.load(f)

    # --------------------------------
    # Build Better Embedding Text
    # --------------------------------
    texts = []

    for item in catalog:

        text = f"""
        Name: {item.get('name', '')}

        Category:
        {' '.join(item.get('keys', []))}

        Job Levels:
        {' '.join(item.get('job_levels', []))}

        Description:
        {item.get('description', '')[:250]}
        """

        texts.append(text)

    # --------------------------------
    # Precompute Catalog Embeddings
    # --------------------------------
    catalog_embeddings = model.encode(texts)

    return catalog

# --------------------------------
# Recommendation Engine
# --------------------------------
def recommend_assessments(state, catalog):

    recommendations = []

    # --------------------------------
    # Build User Query
    # --------------------------------
    query_parts = []

    query_parts.extend(state["skills"])

    if state["seniority"]:
        query_parts.append(state["seniority"])

    if state["personality"]:
        query_parts.append(
            "communication leadership teamwork"
        )

    query = " ".join(query_parts)

    # --------------------------------
    # Query Embedding
    # --------------------------------
    query_embedding = model.encode([query])

    similarities = cosine_similarity(
        query_embedding,
        catalog_embeddings
    )[0]

    # --------------------------------
    # Process Catalog
    # --------------------------------
    for idx, item in enumerate(catalog):

        semantic_score = similarities[idx]

        rule_score = 0

        text = (
            item.get("name", "") + " " +
            item.get("description", "")
        ).lower()

        keys = [
            key.lower()
            for key in item.get("keys", [])
        ]

        job_levels = [
            level.lower()
            for level in item.get(
                "job_levels",
                []
            )
        ]

        # --------------------------------
        # Skill Matching Boost
        # --------------------------------
        matched_skills = 0

        for skill in state["skills"]:

            if skill.lower() in text:
                matched_skills += 1

        rule_score += matched_skills * 0.15

        # --------------------------------
        # Personality Boost
        # --------------------------------
        if state["personality"]:

            personality_categories = [
                "personality & behavior",
                "competencies",
                "development & 360"
            ]

            if any(
                category in keys
                for category in personality_categories
            ):
                rule_score += 0.20

        # --------------------------------
        # Technical Role Boost
        # --------------------------------
        technical_skills = [
            "python",
            "java",
            "c++",
            "sql",
            "javascript",
            "backend developer",
            "frontend developer",
            "software engineer",
            "machine learning"
        ]

        if any(
            skill in state["skills"]
            for skill in technical_skills
        ):

            if (
                "knowledge & skills" in keys or
                "simulations" in keys
            ):
                rule_score += 0.15

        # --------------------------------
        # Simulation Boost
        # --------------------------------
        if (
            "developer" in query or
            "engineer" in query or
            "programming" in query
        ):

            if "simulations" in keys:
                rule_score += 0.20

        # --------------------------------
        # Seniority Boost
        # --------------------------------
        seniority = state.get("seniority")

        if seniority:

            if (
                seniority == "entry-level" and
                (
                    "entry-level" in job_levels or
                    "graduate" in job_levels
                )
            ):
                rule_score += 0.15

            elif (
                seniority == "mid-professional" and
                "mid-professional" in job_levels
            ):
                rule_score += 0.15

            elif (
                seniority == "senior" and
                (
                    "manager" in job_levels or
                    "director" in job_levels
                )
            ):
                rule_score += 0.15

        # --------------------------------
        # Adaptive Assessment Boost
        # --------------------------------
        if item.get("adaptive", "no") == "yes":
            rule_score += 0.03

        # --------------------------------
        # Remote Friendly Boost
        # --------------------------------
        if item.get("remote", "no") == "yes":
            rule_score += 0.02

        # --------------------------------
        # Final Hybrid Score
        # --------------------------------
        final_score = (
            semantic_score * 0.65 +
            rule_score * 0.35
        )

        # --------------------------------
        # Threshold Filtering
        # --------------------------------
        if final_score >= 0.30:

            recommendations.append({

                "score": round(final_score, 3),

                "name": item.get(
                    "name",
                    "Unknown"
                ),

                "url": item.get(
                    "link",
                    ""
                ),

                "test_type": ", ".join(
                    item.get("keys", [])
                ),

                "duration": item.get(
                    "duration",
                    "N/A"
                ),

                "remote_support": item.get(
                    "remote",
                    "no"
                ),

                "adaptive_support": item.get(
                    "adaptive",
                    "no"
                )
            })

    # --------------------------------
    # Sort by Score
    # --------------------------------
    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # --------------------------------
    # Remove Duplicates
    # --------------------------------
    final_results = []

    seen_urls = set()

    for item in recommendations:

        if item["url"] not in seen_urls:

            final_results.append(item)

            seen_urls.add(item["url"])

    return final_results[:10]