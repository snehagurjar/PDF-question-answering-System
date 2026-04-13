from PyPDF2 import PdfReader

# 🔹 Process PDF (NO FAISS, NO EMBEDDINGS)
def process_pdf(filepath):
    reader = PdfReader(filepath)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    print("📊 Extracted text length:", len(text))

    # 🔥 split into chunks (paragraphs)
    chunks = text.split("\n\n")  # paragraph split

    # clean
    chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 50]

    return chunks
    # 🔹 Ask Question (simple logic)
def ask_question(question, chunks):
    question = question.lower()

    stopwords = {"what", "is", "the", "a", "an", "of", "to", "in", "and", "for", "are"}

    keywords = [
        word for word in question.split()
        if word not in stopwords and len(word) > 2
    ]

    best_line = ""
    best_score = 0

    for chunk in chunks:
        lines = chunk.split("\n")

        for line in lines:
            line = line.strip()
            line_lower = line.lower()

            # ❌ Skip useless lines
            if (
                len(line) < 40 or
                line_lower.startswith("q") or
                "interview" in line_lower or
                "example" in line_lower
            ):
                continue

            score = 0

            # 🔥 Exact keyword match (important)
            for word in keywords:
                if word in line_lower:
                    score += 10

            # 🔥 Strong boost if full term exists
            if " ".join(keywords) in line_lower:
                score += 30

            # 🔥 Penalty for unrelated keywords
            unrelated_words = ["primary key", "durability", "normalization"]
            for uw in unrelated_words:
                if uw in line_lower and uw not in question:
                    score -= 5

            if score > best_score:
                best_score = score
                best_line = line

    if not best_line or best_score < 10:
        return "⚠️ No relevant answer found"

    # 🔥 CLEAN ANSWER
    best_line = best_line.replace("Ans :", "").replace("Ans:", "")

    return best_line.strip()