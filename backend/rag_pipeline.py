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

    stopwords = {"what", "is", "the", "a", "an", "of", "to", "in", "and", "for"}

    keywords = [
        word.lower()
        for word in question.split()
        if word.lower() not in stopwords and len(word) > 3
    ]

    lines = text.split("\n")
    matched_lines = []

    for line in lines:
        for word in keywords:
            if word in line.lower():
                matched_lines.append(line)
                break

    if matched_lines:
        return "\n".join(matched_lines[:5])

    return "⚠️ No relevant answer found"