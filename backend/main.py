from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import WEBSITE_URL, WEBSITE_NAME, MAX_PAGES
from crawler import crawl_website
from llm import ask_llm
from cache import website_cache

app = FastAPI(
    title="Website Chatbot API",
    version="1.0.0"
)

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "status": "running",
        "website": WEBSITE_NAME,
        "url": WEBSITE_URL,
        "cached": WEBSITE_URL in website_cache
    }


@app.post("/chat")
def chat(request: ChatRequest):

    # Crawl website only once
    if WEBSITE_URL not in website_cache:

        print(f"Crawling {WEBSITE_NAME}...")

        website_cache[WEBSITE_URL] = crawl_website(
            WEBSITE_URL,
            max_pages=MAX_PAGES
        )

        print("Website cached successfully.")

    answer = ask_llm(
        request.question,
        website_cache[WEBSITE_URL]
    )

    return {
        "answer": answer
    }