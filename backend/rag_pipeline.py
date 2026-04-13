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

    stopwords = {"what", "is", "the", "a", "an", "of", "to", "in", "and", "for"}

    keywords = [
        word for word in question.split()
        if word not in stopwords and len(word) > 2
    ]

    best_chunk = ""
    best_score = 0

    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = 0

        # 🔥 HIGH PRIORITY: full question match
        if question in chunk_lower:
            score += 100

        # 🔥 MEDIUM PRIORITY: keyword match
        for word in keywords:
            if word in chunk_lower:
                score += 5

        # 🔥 EXTRA: multiple occurrences
        for word in keywords:
            score += chunk_lower.count(word)

        if score > best_score:
            best_score = score
            best_chunk = chunk

    if not best_chunk:
        return "⚠️ No relevant answer found"

    # 🔥 CLEAN ANSWER
    lines = best_chunk.split("\n")
    useful_lines = []

    for line in lines:
        line = line.strip()
        line_lower = line.lower()

        if (
            len(line) < 40 or
            line_lower.startswith("q") or
            "interview" in line_lower
        ):
            continue

        line = line.replace("Ans :", "").replace("Ans:", "")
        useful_lines.append(line)

    # remove duplicates
    clean_lines = []
    for line in useful_lines:
        if line not in clean_lines:
            clean_lines.append(line)

    return " ".join(clean_lines[:4])