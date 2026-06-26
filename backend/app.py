from fastapi import FastAPI
from pydantic import BaseModel

from crawler import crawl_website
from llm import ask_llm
from cache import website_cache

app = FastAPI()


class ChatRequest(BaseModel):
    url: str
    question: str


@app.get("/")
def home():
    return {
        "message": "Website Chatbot API is running!"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    if request.url not in website_cache:

        print("Crawling website...")

        website_cache[request.url] = crawl_website(
            request.url,
            max_pages=50
        )

    answer = ask_llm(
        request.question,
        website_cache[request.url]
    )

    return {
        "answer": answer
    }