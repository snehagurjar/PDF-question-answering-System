# from PyPDF2 import PdfReader

# # 🔹 Process PDF
# def process_pdf(filepath):
#     reader = PdfReader(filepath)

#     text = ""
#     for page in reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"

#     print("📊 Extracted text length:", len(text))

#     # 🔥 split into paragraphs
#     chunks = text.split("\n\n")

#     chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 50]

#     return chunks


# # 🔹 Ask Question (UPDATED - NO retriever)
# def ask_question(question, chunks):
#     question = question.lower()

#     keywords = [w for w in question.split() if len(w) > 2]

#     best_answer = ""
#     best_score = 0

#     for chunk in chunks:
#         lines = chunk.split("\n")

#         for i, line in enumerate(lines):
#             line_lower = line.lower()

#             if any(k in line_lower for k in keywords):

#                 score = sum(1 for k in keywords if k in line_lower)

#                 answer = ""
#                 for j in range(i+1, min(i+5, len(lines))):
#                     next_line = lines[j].strip()

#                     if len(next_line) < 20:
#                         continue

#                     if next_line.lower().startswith("q"):
#                         break

#                     answer += next_line + " "

#                 if score > best_score and answer:
#                     best_score = score
#                     best_answer = answer.strip()

#     if best_answer:
#         return best_answer

#     return "⚠️ No relevant answer found"

from PyPDF2 import PdfReader
# 🔥 STEP 1: YAHI ADD KARNA HAI
from sentence_transformers import SentenceTransformer
import numpy as np

# 🔥 MODEL LOAD (GLOBAL)
model = SentenceTransformer("all-MiniLM-L6-v2")
def process_pdf(filepath):
    reader = PdfReader(filepath)

    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"

    chunks = []
    current = ""

    for line in text.split("\n"):
        if len(current) < 300:
            current += " " + line
        else:
            chunks.append(current.strip())
            current = line

    if current:
        chunks.append(current.strip())

    # 🔥 embeddings store करो
    embeddings = model.encode(chunks)

    return {"chunks": chunks, "embeddings": embeddings}
def ask_question(question, data):
    chunks = data["chunks"]
    embeddings = data["embeddings"]

    q_embedding = model.encode(question)

    best_index = -1
    best_score = -1

    for i, emb in enumerate(embeddings):
        score = np.dot(q_embedding, emb) / (
            np.linalg.norm(q_embedding) * np.linalg.norm(emb)
        )

        if score > best_score:
            best_score = score
            best_index = i

    if best_index == -1:
        return "⚠️ No relevant answer found"

    return format_answer(chunks[best_index])
def format_answer(text):
    text = text.strip()

    # 🔥 remove junk
    text = text.replace("\n", " ")

    # 🔥 split into sentences
    sentences = text.split(". ")

    clean = []
    for s in sentences:
        if len(s) > 30:
            clean.append(s.strip())

    # 🔥 limit length
    return "👉 " + ". ".join(clean[:4])