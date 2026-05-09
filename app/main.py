from fastapi import FastAPI
from app.models import ChatRequest
from app.utils import build_state
from app.reply_builder import build_reply
from app.compare import compare_assessments
from app.recommender import (
    load_catalog,
    recommend_assessments
)

app = FastAPI()
catalog = load_catalog()

# --------------------------------
# Health Endpoint
# --------------------------------
@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# --------------------------------
# Off-topic Detection
# --------------------------------
def is_off_topic(text):
    text = text.lower()
    blocked_topics = [
        "salary",
        "movie",
        "politics",
        "weather",
        "sports",
        "legal advice",
        "investment",
        "stock market"
    ]
    return any(topic in text for topic in blocked_topics)

# --------------------------------
# Comparison Detection
# --------------------------------
def is_comparison_request(text):
    text = text.lower()
    comparison_words = [
        "difference",
        "compare",
        "vs",
        "versus"
    ]
    return any(word in text for word in comparison_words)

# --------------------------------
# Clean Recommendation Output
# --------------------------------
def clean_recommendations(recommendations):
    cleaned = []
    seen_urls = set()
    for item in recommendations:
        url = item["url"]
        # Remove duplicates
        if url in seen_urls:
            continue
        seen_urls.add(url)
        cleaned.append({
            "name": item["name"],
            "url": url,
            "test_type": item["test_type"]
        })
    return cleaned[:10]

# --------------------------------
# Chat Endpoint
# --------------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    # --------------------------------
    # Empty Messages
    # --------------------------------
    if not request.messages:
        return {
            "reply": (
                "Please share the role, skill, "
                "or hiring requirement you have."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    latest_message = (request.messages[-1].content.strip())

    # --------------------------------
    # Very Short Input
    # --------------------------------
    if len(latest_message) < 3:
        return {
            "reply": (
                "Please share the role, technology, "
                "or assessment requirement."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # --------------------------------
    # Off-topic Request
    # --------------------------------
    if is_off_topic(latest_message):

        return {
            "reply": (
                "I can only help with SHL "
                "assessment recommendations "
                "and comparisons."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # --------------------------------
    # Comparison Request
    # --------------------------------
    if is_comparison_request(latest_message):
        comparison_result = compare_assessments(
            latest_message,
            catalog
        )
        return {
            "reply": comparison_result,
            "recommendations": [],
            "end_of_conversation": False
        }
    # --------------------------------
    # Build State
    # --------------------------------
    state = build_state(request.messages)

    # --------------------------------
    # Missing Skills
    # --------------------------------
    if not state["skills"]:
        return {
            "reply": (
                "Could you tell me which role, "
                "technology, or skill set "
                "you are hiring for?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # --------------------------------
    # Missing Seniority
    # --------------------------------
    if not state["seniority"]:
        return {
            "reply": (
                "Could you share the seniority "
                "level or years of experience "
                "required for the role?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # --------------------------------
    # Generate Recommendations
    # --------------------------------
    recommendations = recommend_assessments(state, catalog)
    cleaned_recommendations = (clean_recommendations(recommendations))

    # --------------------------------
    # No Matches
    # --------------------------------
    if not cleaned_recommendations:
        return {
            "reply": (
                "I could not find strong SHL "
                "assessment matches for the "
                "current requirements. "
                "Could you share more details "
                "about the role or skills needed?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # --------------------------------
    # Final Response
    # --------------------------------
    return {
        "reply": build_reply(
            state,
            cleaned_recommendations
        ),
        "recommendations": cleaned_recommendations,
        "end_of_conversation": True
    }