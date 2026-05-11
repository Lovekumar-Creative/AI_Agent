from fastapi import FastAPI
import re

from app.models import ChatRequest
from app.utils import build_state
from app.reply_builder import build_reply
from app.compare import compare_assessments

from app.recommender import (
    load_catalog,
    recommend_assessments
)

# --------------------------------
# FastAPI App
# --------------------------------
app = FastAPI(
    title="SHL Assessment Recommendation API"
)

# --------------------------------
# Load Catalog Once
# --------------------------------
catalog = load_catalog()

# --------------------------------
# Health Endpoint
# --------------------------------
@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "SHL Assessment Recommendation API"
    }

# --------------------------------
# Greeting Detection
# --------------------------------
def is_greeting(text):

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening",
        "good afternoon"
    ]

    text = text.lower().strip()

    words = re.findall(r'\b\w+\b', text)

    return any(greeting in words for greeting in greetings)

# --------------------------------
# Off-topic Detection
# --------------------------------
def is_off_topic(text):
    text = text.lower()

    blocked_topics = [
        "movie",
        "weather",
        "sports",
        "bitcoin",
        "crypto",
        "ipl score",
        "football",
        "politics"
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
# Role Intent Detection
# --------------------------------
ROLE_WORDS = [
    "developer",
    "engineer",
    "analyst",
    "tester",
    "architect",
    "manager",
    "administrator",
    "consultant"
]

def has_role_intent(text):
    text = text.lower()

    return any(role in text for role in ROLE_WORDS)

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
            "test_type": item["test_type"],
            "duration": item.get("duration", "N/A"),
            "remote_support": item.get(
                "remote_support",
                "no"
            ),
            "adaptive_support": item.get(
                "adaptive_support",
                "no"
            )
        })

    return cleaned[:10]

# --------------------------------
# Clarification Logic
# --------------------------------
def get_missing_field_response(
    state,
    latest_message
):

    # --------------------------------
    # No Skills + No Role
    # --------------------------------
    if (
        len(state["skills"]) == 0
        and not has_role_intent(latest_message)
    ):

        return (
            "Could you share the role, "
            "technology, or skill set "
            "you are hiring for?"
        )

    return None

# --------------------------------
# Chat Endpoint
# --------------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # --------------------------------
        # Empty Conversation
        # --------------------------------
        if not request.messages:

            return {
                "reply": (
                    "Please share the role, "
                    "skills, or hiring "
                    "requirements."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # --------------------------------
        # Latest User Message
        # --------------------------------
        latest_message = (
            request.messages[-1]
            .content
            .strip()
        )

        # --------------------------------
        # Very Short Input
        # --------------------------------
        if len(latest_message) < 2:

            return {
                "reply": (
                    "Please provide more "
                    "details about the "
                    "hiring requirement."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # --------------------------------
        # Greeting Handling
        # --------------------------------
        if is_greeting(latest_message):

            return {
                "reply": (
                    "Hello! I can help you "
                    "find relevant SHL "
                    "assessments based on "
                    "job roles, technologies, "
                    "skills, and experience "
                    "levels."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # --------------------------------
        # Off-topic Handling
        # --------------------------------
        if is_off_topic(latest_message):

            return {
                "reply": (
                    "I can help only with "
                    "SHL assessment "
                    "recommendations and "
                    "assessment comparisons."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # --------------------------------
        # Assessment Comparison
        # --------------------------------
        if is_comparison_request(latest_message):

            comparison_result = (
                compare_assessments(
                    latest_message,
                    catalog
                )
            )

            return {
                "reply": comparison_result,
                "recommendations": [],
                "end_of_conversation": False
            }

        # --------------------------------
        # Build Conversation State
        # --------------------------------
        state = build_state(
            request.messages
        )

        # --------------------------------
        # Clarification Flow
        # --------------------------------
        clarification = (
            get_missing_field_response(
                state,
                latest_message
            )
        )

        if clarification:

            return {
                "reply": clarification,
                "recommendations": [],
                "end_of_conversation": False
            }

        # --------------------------------
        # Generate Recommendations
        # --------------------------------
        recommendations = (
            recommend_assessments(
                state,
                catalog
            )
        )

        # --------------------------------
        # Filter Weak Matches
        # --------------------------------
        recommendations = [
            item for item in recommendations
            if item["score"] >= 0.40
        ]

        # --------------------------------
        # Clean Recommendations
        # --------------------------------
        cleaned_recommendations = (
            clean_recommendations(
                recommendations
            )
        )

        # --------------------------------
        # No Recommendations Found
        # --------------------------------
        if not cleaned_recommendations:

            return {
                "reply": (
                    "I could not find highly "
                    "relevant SHL assessments "
                    "for the current hiring "
                    "requirements.\n\n"
                    "Please share:\n"
                    "- technologies or skills\n"
                    "- experience level\n"
                    "- role type\n"
                    "- technical or behavioral focus"
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

            "recommendations":
                cleaned_recommendations,

            "end_of_conversation": True
        }

    # --------------------------------
    # Exception Handling
    # --------------------------------
    except Exception:

        return {
            "reply": (
                "An internal processing "
                "error occurred while "
                "generating recommendations."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }