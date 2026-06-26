import re


def split_into_paragraphs(text):
    """
    Split page into logical paragraphs.
    """

    paragraphs = re.split(r"\n\s*\n|\r\n\s*\r\n", text)

    cleaned = []

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if len(paragraph) > 40:
            cleaned.append(paragraph)

    return cleaned


def score_paragraph(paragraph, keywords):
    """
    Score paragraph based on keyword frequency.
    """

    paragraph_lower = paragraph.lower()

    score = 0

    for keyword in keywords:

        score += paragraph_lower.count(keyword.lower())

    return score


def extract_snippets(question, page, max_snippets=5):
    """
    Extract only the most relevant paragraphs from a page.
    """

    keywords = re.findall(r"[a-zA-Z0-9]+", question.lower())

    paragraphs = split_into_paragraphs(page["text"])

    scored = []

    for paragraph in paragraphs:

        score = score_paragraph(paragraph, keywords)

        if score > 0:
            scored.append((score, paragraph))

    scored.sort(reverse=True, key=lambda x: x[0])

    snippets = []

    for _, paragraph in scored[:max_snippets]:
        snippets.append(paragraph)

    return "\n\n".join(snippets)