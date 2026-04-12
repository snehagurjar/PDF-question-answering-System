
from PyPDF2 import PdfReader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.llms import HuggingFacePipeline

# # ✅ Stable LLM (longer answers)
# llm = HuggingFacePipeline.from_model_id(
#     model_id="gpt2",
#     task="text-generation",
#     pipeline_kwargs={
#         "max_new_tokens": 150,
#         "temperature": 0.2,
#         "do_sample": False,
#         "repetition_penalty": 1.2
#     }
# )

# 🔹 Process PDF
def process_pdf(filepath):
    reader = PdfReader(filepath)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    print("📊 Extracted text length:", len(text))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,   # 🔥 increased (better context)
        chunk_overlap=40
    )

    chunks = splitter.create_documents([text])

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store.as_retriever(search_kwargs={"k": 4})  # 🔥 more chunks

def format_answer(text):
    text = text.strip()

    # 🔹 Add proper line breaks
    text = text.replace("•", "\n•")
    text = text.replace("1.", "\n1.")
    text = text.replace("2.", "\n2.")
    text = text.replace("3.", "\n3.")
    text = text.replace("4.", "\n4.")
    text = text.replace("5.", "\n5.")

    # 🔹 Add sections
    text = text.replace("Flow:", "\n\nFlow:\n")
    text = text.replace("Example:", "\n\nExample:\n")
    text = text.replace("Key Points:", "\n\nKey Points:\n")

    # 🔹 Clean extra spaces
    text = " ".join(text.split())

    return text.strip()
def ask_question(question, retriever):
    docs = retriever.get_relevant_documents(question)

    if not docs:
        return "⚠️ No relevant answer found in PDF"

    # 🔥 combine context
    context = " ".join([doc.page_content for doc in docs])
    context = context.replace("\n", " ").strip()
    context = context[:1200]

    print("📚 Context:", context)

    # 🔥 OPTIONAL: try extracting clean answer (Ans:)
    answer = ""

    if "Ans :" in context:
        answer = context.split("Ans :")[1]
    elif "Ans:" in context:
        answer = context.split("Ans:")[1]
    elif "Answer:" in context:
        answer = context.split("Answer:")[1]

    if answer:
        if "Q" in answer:
            answer = answer.split("Q")[0]

        answer = answer.strip()
        answer = " ".join(answer.split())

        return format_answer(answer[:600])

    # 🔥 fallback → use full context
    return format_answer(context[:800])