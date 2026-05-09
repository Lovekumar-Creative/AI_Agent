# SHL Conversational Assessment Recommender

A FastAPI-based conversational agent built for the SHL AI Intern take-home assignment. The system helps recruiters and hiring managers discover relevant SHL assessments through multi-turn conversations using grounded catalog-based retrieval. The agent supports clarification, recommendation, refinement, comparison, and off-topic refusal while maintaining a fully stateless architecture.

## Features

- Clarifies vague hiring queries before recommending assessments
- Recommends 1–10 grounded SHL assessments
- Supports conversational refinement like “Actually add personality tests”
- Compares SHL assessments using catalog data
- Refuses off-topic and non-SHL requests
- Uses only official SHL catalog URLs
- Stateless API design using full conversation history

## Tech Stack

- Python
- FastAPI
- Pydantic
- JSON-based retrieval system

## Project Structure

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
├── Procfile
└── README.md