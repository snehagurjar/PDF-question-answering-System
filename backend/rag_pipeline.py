from PyPDF2 import PdfReader

# 🔹 Process PDF
def process_pdf(filepath):
    reader = PdfReader(filepath)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    print("📊 Extracted text length:", len(text))

    # 🔥 split into paragraphs
    chunks = text.split("\n\n")

    chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 50]

    return chunks


# 🔹 Ask Question (UPDATED - NO retriever)
def ask_question(question, chunks):
    question = question.lower()

    keywords = [w for w in question.split() if len(w) > 2]

    best_answer = ""
    best_score = 0

    for chunk in chunks:
        lines = chunk.split("\n")

        for i, line in enumerate(lines):
            line_lower = line.lower()

            if any(k in line_lower for k in keywords):

                score = sum(1 for k in keywords if k in line_lower)

                answer = ""
                for j in range(i+1, min(i+5, len(lines))):
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









# from PyPDF2 import PdfReader
# import requests
# import numpy as np
# import os

# # 🔥 HF API
# API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
# HEADERS = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}


# # 🔹 get embedding from API (SAFE)
# def get_embedding(text):
#     try:
#         response = requests.post(API_URL, headers=HEADERS, json={"inputs": text})

#         if response.status_code == 200:
#             data = response.json()
#             if isinstance(data, list):
#                 return data[0]

#         # 🔥 fallback (keyword based)
#         return None

#     except:
#         return None
# def process_pdf(filepath):
#     reader = PdfReader(filepath)

#     text = ""
#     for page in reader.pages:
#         if page.extract_text():
#             text += page.extract_text() + "\n"

#     chunks = []
#     current = ""

#     for line in text.split("\n"):
#         if len(current) < 150:
#             current += " " + line
#         else:
#             chunks.append(current.strip())
#             current = line

#     if current:
#         chunks.append(current.strip())

#     # 🔥 embeddings generate ONCE
#     embeddings = []

#     for chunk in chunks:
#         emb = get_embedding(chunk)
#         if emb is not None:
#             embeddings.append(emb)
#         else:
#             embeddings.append([0.0] * 384)

#     return {
#         "chunks": chunks,
#         "embeddings": embeddings
#     }


# # 🔹 Ask Question (FAST + SEMANTIC)
# def ask_question(question, data):
#     chunks = data["chunks"]
#     embeddings = data["embeddings"]

#     q_embedding = get_embedding(question)

#     if q_embedding is None:
#         return "⚠️ Embedding API error"

#     best_score = -1
#     best_chunk = ""

#     # 🔥 find best chunk
#     for i, emb in enumerate(embeddings):
#         if emb is None:
#             continue

#         score = np.dot(q_embedding, emb) / (
#             np.linalg.norm(q_embedding) * np.linalg.norm(emb)
#         )

#         if score > best_score:
#             best_score = score
#             best_chunk = chunks[i]

#     if not best_chunk:
#         return "⚠️ No relevant answer found"

#     # 🔥 STEP 2: extract relevant lines
#     question = question.lower()
#     keywords = [w for w in question.split() if len(w) > 2]

#     lines = best_chunk.split("\n")

#     answer = ""
#     for line in lines:
#         line_lower = line.lower()

#         if any(k in line_lower for k in keywords):
#             answer += line.strip() + " "

#     # 🔥 अगर कुछ नहीं मिला
#     if not answer:
#         answer = best_chunk[:300]

#     return format_answer(answer)
# def format_answer(text):
#     text = text.strip()
#     text = text.replace("\n", " ")

#     sentences = text.split(". ")

#     clean = []
#     for s in sentences:
#         if len(s) > 20:
#             clean.append(s.strip())

#     return "👉 " + ". ".join(clean[:3])