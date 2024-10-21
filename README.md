# TLDR

Kalygo 3.0 CrewAI API (powered by FastAPI)

## How to run the FastAPI

- pip install -r requirements.txt
- uvicorn src.main:app --host 0.0.0.0 --port 5000 --proxy-headers --reload

## How to save versions of top-level packages

- pip install pipreqs
- pipreqs . --force

## For testing

- curl localhost:5000