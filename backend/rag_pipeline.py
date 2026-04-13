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

    # 🔥 STEP 1: find best chunk
    for chunk in chunks:
        score = 0
        chunk_lower = chunk.lower()

        for word in keywords:
            score += chunk_lower.count(word)

        if score > best_score:
            best_score = score
            best_chunk = chunk

    if not best_chunk:
        return "⚠️ No relevant answer found"

    # 🔥 STEP 2: extract useful lines
    lines = best_chunk.split("\n")
    useful_lines = []

    for line in lines:
        line = line.strip()
        line_lower = line.lower()

        # ❌ skip unwanted
        if (
            len(line) < 40 or
            line_lower.startswith("q") or
            "interview" in line_lower or
            "vs" in line_lower
        ):
            continue

        line = line.replace("Ans :", "").replace("Ans:", "")

        useful_lines.append(line)

    # 🔥 STEP 3: remove duplicates
    clean_lines = []
    for line in useful_lines:
        if line not in clean_lines:
            clean_lines.append(line)

    # 🔥 STEP 4: take more lines for complete answer
    final_answer = " ".join(clean_lines[:4])   # 👈 2 → 4 lines

    return final_answer[:700]