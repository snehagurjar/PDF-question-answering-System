# from PyPDF2 import PdfReader

# # 🔹 Process PDF (NO FAISS, NO EMBEDDINGS)
# def process_pdf(filepath):
#     reader = PdfReader(filepath)

#     text = ""
#     for page in reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"

#     print("📊 Extracted text length:", len(text))

#     # 🔥 split into chunks (paragraphs)
#     chunks = text.split("\n\n")  # paragraph split

#     # clean
#     chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 50]

#     return chunks
#     # 🔹 Ask Question (simple logic)
# def ask_question(question, retriever):
#     docs = retriever.get_relevant_documents(question)

#     if not docs:
#         return "⚠️ No relevant answer found"

#     question = question.lower()
#     keywords = [w for w in question.split() if len(w) > 2]

#     for doc in docs:
#         lines = doc.page_content.split("\n")

#         for i, line in enumerate(lines):
#             line_lower = line.lower()

#             if any(k in line_lower for k in keywords):

#                 answer = ""
#                 for j in range(i+1, min(i+5, len(lines))):
#                     next_line = lines[j].strip()

#                     if next_line.lower().startswith("q"):
#                         break

#                     answer += next_line + " "

#                 if answer:
#                     return answer.strip()

#     return "⚠️ No relevant answer found"

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