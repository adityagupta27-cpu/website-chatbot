import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import (
    WEBSITE_URL,
    WEBSITE_NAME,
    MAX_PAGES,
    CACHE_FILE
)

from crawler import (
    crawl_website,
    save_cache,
    load_cache
)

from llm import ask_llm
from cache import website_cache


# Create FastAPI FIRST
app = FastAPI(
    title="Website Chatbot API",
    version="2.0.0"
)

# THEN add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://website-chatbot.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from pydantic import BaseModel

from config import (
    WEBSITE_URL,
    WEBSITE_NAME,
    MAX_PAGES,
    CACHE_FILE
)

from crawler import (
    crawl_website,
    save_cache,
    load_cache
)

from llm import ask_llm
from cache import website_cache


app = FastAPI(
    title="Website Chatbot API",
    version="2.0.0"
)


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://website-chatbot.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Model
# -----------------------------

class ChatRequest(BaseModel):
    question: str


# -----------------------------
# Startup
# -----------------------------

@app.on_event("startup")
def startup():

    print("\nStarting Website Chatbot...\n")

    if os.path.exists(CACHE_FILE):

        print("Loading cached website...")

        website_cache[WEBSITE_URL] = load_cache()

        print("Knowledge base loaded.\n")

    else:

        print("No cache found.")
        print("Building knowledge base...\n")

        pages = crawl_website(
            WEBSITE_URL,
            max_pages=MAX_PAGES
        )

        save_cache(pages)

        website_cache[WEBSITE_URL] = pages

        print("\nKnowledge base created.\n")


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():

    return {

        "status": "running",

        "website": WEBSITE_NAME,

        "cached": WEBSITE_URL in website_cache,

        "pages": len(
            website_cache.get(
                WEBSITE_URL,
                []
            )
        )

    }
# -----------------------------
# Chat
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    if WEBSITE_URL not in website_cache:

        return {
            "answer": "Knowledge base is not loaded yet."
        }

    answer = ask_llm(
        request.question,
        website_cache[WEBSITE_URL]
    )

    return {
        "answer": answer
    }


# -----------------------------
# Refresh Website
# -----------------------------

@app.post("/refresh")
def refresh():

    print("\nRefreshing knowledge base...\n")

    pages = crawl_website(
        WEBSITE_URL,
        max_pages=MAX_PAGES
    )

    save_cache(pages)

    website_cache[WEBSITE_URL] = pages

    return {

        "status": "success",

        "message": "Knowledge base refreshed successfully.",

        "pages": len(pages)

    }


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "website": WEBSITE_NAME,

        "cache_loaded": WEBSITE_URL in website_cache,

        "pages_loaded": len(
            website_cache.get(
                WEBSITE_URL,
                []
            )
        )

    }