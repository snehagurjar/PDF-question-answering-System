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

    best_chunk = ""
    best_line_index = 0
    best_score = 0

    for chunk in chunks:
        lines = chunk.split("\n")

        for i, line in enumerate(lines):
            line_clean = line.strip()
            line_lower = line_clean.lower()

            if len(line_clean) < 30:
                continue

            score = 0

            for word in keywords:
                if word in line_lower:
                    score += 10

            if any(x in line_lower for x in [" is ", " are ", " refers to"]):
                score += 20

            if score > best_score:
                best_score = score
                best_chunk = lines
                best_line_index = i

    if not best_chunk:
        return "⚠️ No relevant answer found"

    # 🔥 TAKE 3-4 LINES FROM BEST POSITION
    answer_lines = best_chunk[best_line_index : best_line_index + 4]

    clean_lines = []
    for line in answer_lines:
        line = line.strip()

        if (
            len(line) < 20 or
            line.lower().startswith("q")
        ):
            continue

        line = line.replace("Ans :", "").replace("Ans:", "")

        clean_lines.append(line)

    return "👉 " + " ".join(clean_lines)