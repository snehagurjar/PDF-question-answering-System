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
        score = 0
        chunk_lower = chunk.lower()

        for word in keywords:
            if word in chunk_lower:
                # score += 1
                score += chunk_lower.count(word)

        if score > best_score:
            best_score = score
            best_chunk = chunk

    if best_chunk:
        return best_chunk[:800]

    return "⚠️ No relevant answer found"