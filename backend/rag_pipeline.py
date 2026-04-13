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

    best_lines = []
    best_score = 0

    # 🔥 STEP 1: loop through all lines (NOT chunks)
    for chunk in chunks:
        lines = chunk.split("\n")

        for line in lines:
            line_clean = line.strip()
            line_lower = line_clean.lower()

            if len(line_clean) < 30:
                continue

            score = 0

            # 🔥 exact keyword match
            for word in keywords:
                if word in line_lower:
                    score += 10

            # 🔥 boost important terms
            if any(word in line_lower for word in keywords):
                score += 5

            if score > best_score:
                best_score = score
                best_lines = [line_clean]

            elif score == best_score and score != 0:
                best_lines.append(line_clean)

    if not best_lines:
        return "⚠️ No relevant answer found"

    # 🔥 STEP 2: clean answer
    final_lines = []

    for line in best_lines:
        if line.lower().startswith("q"):
            continue

        line = line.replace("Ans :", "").replace("Ans:", "")

        if line not in final_lines:
            final_lines.append(line)

    # 🔥 STEP 3: return combined answer
    return " ".join(final_lines[:3])