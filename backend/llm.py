import os
from dotenv import load_dotenv

import google.generativeai as genai
from google.generativeai.types import GenerationConfig

from retriever import retrieve

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

generation_config = GenerationConfig(
    temperature=0.3,
    max_output_tokens=4190,
)


def detect_intent(question):
    """
    Determine how Gemini should format the answer.
    """

    question = question.lower()

    if any(word in question for word in [
        "list",
        "services",
        "features",
        "products",
        "technologies",
        "capabilities"
    ]):
        return "list"

    if any(word in question for word in [
        "explain",
        "describe",
        "how",
        "why",
        "tell me about"
    ]):
        return "explanation"

    if any(word in question for word in [
        "summary",
        "summarize",
        "overview"
    ]):
        return "summary"

    return "normal"


def get_response_style(intent):
    styles = {

        "list": """
Return the answer as concise bullet points.

Each bullet should contain one important point.

Avoid long paragraphs.
""",

        "explanation": """
Explain clearly.

Use 2-3 short paragraphs.

Keep it under 200 words.

Avoid repetition.
""",

        "summary": """
Summarize in 5-8 bullet points.

Highlight only the most important information.
""",

        "normal": """
Answer naturally.

Keep the answer informative and concise.

Use paragraphs if appropriate.
"""
    }

    return styles[intent]


def ask_llm(question, pages):
    """
    Ask Gemini using only the supplied website content.
    """

    relevant_pages = retrieve(
        question,
        pages,
        top_k=6
    )

    context = []

    for page in relevant_pages:

        page_text = page["text"][:6000]

        context.append(
            f"""
Source:
{page['url']}

{page_text}
"""
        )

    website_text = "\n\n".join(context)

    intent = detect_intent(question)
    response_style = get_response_style(intent)

    prompt = f"""
You are an AI assistant for a company website.

Your job is to answer user questions ONLY using the provided website information.

Rules:

1. Use ONLY the information provided below.
2. Never invent facts or use outside knowledge.
3. If the answer cannot be found, reply exactly:
   "I couldn't find that information on the website."

Answer Guidelines:

- Write answers that are detailed enough to fully answer the question.
- Aim for approximately 150–250 words when appropriate.
- If the answer contains multiple items, use bullet points.
- Briefly explain each bullet point instead of only listing it.
- Avoid repeating the same information.
- Keep a professional and readable style.
- Use Markdown formatting where appropriate.

Formatting Instructions:

{response_style}

Relevant Website Sections:

{website_text}

--------------------------------------------------

User Question:

{question}
"""

    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    return response.text.strip()


if __name__ == "__main__":

    with open("website_content.txt", "r", encoding="utf-8") as f:
        website_text = f.read()

    question = "What services does this company provide?"

    answer = ask_llm(question, website_text)

    print("\nAnswer:\n")
    print(answer)