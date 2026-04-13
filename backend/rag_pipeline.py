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
def ask_question(question, retriever):
    docs = retriever.get_relevant_documents(question)

    if not docs:
        return "⚠️ No relevant answer found"

    question = question.lower()
    keywords = [w for w in question.split() if len(w) > 2]

    best_answer = ""
    best_score = 0

    for doc in docs:
        text = doc.page_content

        lines = text.split("\n")

        for i in range(len(lines)):
            line = lines[i].strip()
            line_lower = line.lower()

            # 🔥 find matching question line
            if any(k in line_lower for k in keywords):

                score = 0

                # keyword match
                for k in keywords:
                    if k in line_lower:
                        score += 10

                # exact phrase boost
                if " ".join(keywords) in line_lower:
                    score += 40

                # question format boost
                if "what is" in line_lower or "q" in line_lower:
                    score += 20

                # 🔥 extract NEXT lines as answer
                answer = ""
                for j in range(i+1, min(i+6, len(lines))):
                    next_line = lines[j].strip()

                    if len(next_line) < 20:
                        continue

                    if next_line.lower().startswith("q"):
                        break

                    answer += next_line + " "

                if score > best_score and answer:
                    best_score = score
                    best_answer = answer.strip()

    if best_answer:
        return best_answer

    return "⚠️ No relevant answer found"