from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# --------------------------------
# Load Embedding Model
# --------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# --------------------------------
# Known Skills / Technologies
# --------------------------------
KNOWN_SKILLS = [

    # Programming Languages
    "python",
    "java",
    "c++",
    "c programming",
    "c#",
    "javascript",
    "typescript",

    # Development Roles
    "software engineer",
    "backend developer",
    "frontend developer",
    "full stack developer",
    "web developer",

    # Frontend
    "react",
    "angular",
    "html",
    "css",

    # Backend
    "nodejs",
    "django",
    "flask",
    "spring boot",

    # Database
    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    # Cloud / DevOps
    "aws",
    "cloud computing",
    "docker",
    "kubernetes",
    "devops",

    # Data Science / AI
    "machine learning",
    "deep learning",
    "nlp",
    "data science",
    "data analyst",
    "statistics",
    "pandas",
    "numpy",

    # Big Data
    "hadoop",
    "spark",
    "kafka",
    "hive",

    # Testing
    "selenium",
    "automation testing",
    "agile testing",

    # General
    "agile",
    "computer science"
]

# --------------------------------
# Precompute Embeddings
# --------------------------------
skill_embeddings = model.encode(KNOWN_SKILLS)

# --------------------------------
# Seniority Keywords
# --------------------------------
FRESHER_WORDS = [
    "fresher",
    "entry level",
    "entry-level",
    "graduate",
    "junior",
    "intern"
]

SENIOR_WORDS = [
    "senior",
    "lead",
    "manager",
    "architect",
    "head"
]

# --------------------------------
# Personality Keywords
# --------------------------------
PERSONALITY_WORDS = [
    "communication",
    "leadership",
    "stakeholder",
    "teamwork",
    "collaboration",
    "presentation",
    "client handling",
    "behavior",
    "soft skills"
]

# --------------------------------
# Hybrid Skill Extraction
# --------------------------------
def extract_skills(text):

    text = text.lower()

    detected_skills = set()

    # --------------------------------
    # Exact Keyword Matching
    # --------------------------------
    for skill in KNOWN_SKILLS:

        if skill in text:
            detected_skills.add(skill)

    # --------------------------------
    # Semantic Matching
    # --------------------------------
    query_embedding = model.encode([text])

    similarities = cosine_similarity(
        query_embedding,
        skill_embeddings
    )[0]

    for idx, score in enumerate(similarities):

        if score >= 0.60:
            detected_skills.add(KNOWN_SKILLS[idx])

    return list(detected_skills)

# --------------------------------
# Seniority Detection
# --------------------------------
def detect_seniority(text):

    text = text.lower()

    # Fresher Keywords
    if any(word in text for word in FRESHER_WORDS):
        return "entry-level"

    # Experience Detection
    experience = re.findall(
        r'(\d+)\s*\+?\s*years?',
        text
    )

    if experience:

        years = int(experience[0])

        if years <= 2:
            return "entry-level"

        elif years <= 5:
            return "mid-professional"

        else:
            return "senior"

    # Senior Keywords
    if any(word in text for word in SENIOR_WORDS):
        return "senior"

    return None

# --------------------------------
# Personality Detection
# --------------------------------
def detect_personality(text):

    text = text.lower()

    return any(
        word in text
        for word in PERSONALITY_WORDS
    )

# --------------------------------
# Main Extraction Function
# --------------------------------
def extract_info(text):

    text = text.lower()

    info = {
        "skills": [],
        "seniority": None,
        "personality": False
    }

    # --------------------------------
    # Skills
    # --------------------------------
    info["skills"] = extract_skills(text)

    # --------------------------------
    # Seniority
    # --------------------------------
    info["seniority"] = detect_seniority(text)

    # --------------------------------
    # Personality
    # --------------------------------
    info["personality"] = detect_personality(text)

    return info