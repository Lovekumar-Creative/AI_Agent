---

# 🤖 SHL Conversational Assessment Recommender

An AI-powered conversational recommendation system built using FastAPI for the SHL AI Intern Take-Home Assignment.

The application helps recruiters and hiring managers discover relevant SHL assessments through intelligent multi-turn conversations using grounded catalog-based retrieval.

---

## 🚀 Live Demo

### 🌐 Hugging Face Space

https://aiwithlove2k2-shl-agent.hf.space/

### 📘 Interactive API Docs

https://aiwithlove2k2-shl-agent.hf.space/docs

### ❤️ Health Check

https://aiwithlove2k2-shl-agent.hf.space/health

---

## ✨ Features

* ✅ Conversational SHL assessment recommendation system
* ✅ Multi-turn recruiter interaction support
* ✅ Clarification handling for vague hiring queries
* ✅ Assessment comparison support
* ✅ Off-topic refusal handling
* ✅ Catalog-grounded recommendations only
* ✅ Stateless FastAPI architecture
* ✅ Clean REST API design
* ✅ Docker deployment support


---

## 🧠 Example Queries

* “Need Java developer assessments for 3 years experience”
* “Recommend personality and cognitive tests for sales roles”
* “Compare Verify Interactive and Core Java”
* “Add behavioral assessment as well”

---

## 🛠️ Tech Stack

| Technology     | Usage                            |
| -------------- | -------------------------------- |
| Python         | Backend Programming              |
| FastAPI        | REST API Framework               |
| Pydantic       | Request Validation               |
| Docker         | Deployment                       |
| JSON Retrieval | Assessment Recommendation Engine |

---

## 📂 Project Structure

```text
shl_agent/
│
├── app/
│   ├── main.py
│   ├── recommender.py
│   ├── extractor.py
│   ├── utils.py
│   ├── compare.py
│   ├── reply_builder.py
│   └── models.py
│
├── data/
│   └── shl_catalog.json
│
├── requirements.txt
└── README.md
```

---

## ⚡ API Endpoints

| Endpoint  | Description           |
| --------- | --------------------- |
| `/`       | Root Endpoint         |
| `/health` | Health Check          |
| `/chat`   | Recommendation API    |
| `/docs`   | Swagger Documentation |

---

## 📌 Deployment

This project is deployed on Hugging Face Spaces using Docker and FastAPI.

---

## 👨‍💻 Author

**Love Kumar**

* FastAPI Developer
* AI & Machine Learning Enthusiast
* NLP & Recommendation Systems

---
