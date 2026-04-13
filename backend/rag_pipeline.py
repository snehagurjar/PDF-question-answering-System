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

    best_paragraph = ""
    best_score = 0

    # 🔥 STEP 1: break chunks into paragraphs
    for chunk in chunks:
    paragraphs = chunk.split("\n\n")

    for para in paragraphs:
        para_clean = para.strip()
        para_lower = para_clean.lower()

        if len(para_clean) < 40:
            continue

        score = 0

        # 🔥 1. keyword match
        for word in keywords:
            if word in para_lower:
                score += 10

        # 🔥 2. definition boost
        if any(x in para_lower for x in [" is ", " are ", " refers to", " defined as"]):
            score += 20

        # ✅ 🔥 YAHI ADD KARNA HAI (IMPORTANT)
        if " ".join(keywords) in para_lower:
            score += 40

        # 🔥 3. penalty
        unrelated = ["oop", "inheritance", "polymorphism"]
        for u in unrelated:
            if u in para_lower and u not in question:
                score -= 10

        if score > best_score:
            best_score = score
            best_paragraph = para_clean

    if not best_paragraph or best_score < 15:
        return "⚠️ No relevant answer found"

    # 🔥 CLEAN OUTPUT
    best_paragraph = best_paragraph.replace("Ans :", "").replace("Ans:", "")

    return "👉 " + best_paragraph