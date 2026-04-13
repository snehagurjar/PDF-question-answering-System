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

    return text  # 🔥 return plain text


# 🔹 Ask Question (simple logic)
def ask_question(question, text):
    if not text:
        return "⚠️ No content found in PDF"

    # 🔥 basic keyword search
    question = question.lower()
    lines = text.split("\n")

    matched_lines = []

    for line in lines:
        if any(word in line.lower() for word in question.split()):
            matched_lines.append(line)

    if matched_lines:
        return "\n".join(matched_lines[:10])  # top matches

    return text[:500]  # fallback