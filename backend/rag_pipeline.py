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

    # 🔥 split into lines
    lines = text.split("\n")

    qa_pairs = []
    current_q = ""
    current_a = ""

    for line in lines:
        line = line.strip()

        # detect question
        if line.lower().startswith("q"):
            if current_q and current_a:
                qa_pairs.append((current_q, current_a))

            current_q = line
            current_a = ""

        elif "ans" in line.lower():
            current_a += line + " "

        else:
            if current_a:
                current_a += line + " "

    # add last
    if current_q and current_a:
        qa_pairs.append((current_q, current_a))

    return qa_pairs
# 🔹 Ask Question (simple logic)
def ask_question(question, qa_pairs):
    question = question.lower()

    best_match = ""
    best_score = 0

    for q, a in qa_pairs:
        score = 0

        for word in question.split():
            if word in q.lower():
                score += 1

        if score > best_score:
            best_score = score
            best_match = a

    if best_match:
        return best_match[:500]

    return "⚠️ No relevant answer found"