from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from rag_pipeline import process_pdf, ask_question

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

retriever_store = {}

@app.route("/")
def home():
    return "Backend running 🚀"


@app.route("/upload", methods=["POST"])
def upload():
    try:
        global retriever_store   # 🔥 IMPORTANT

        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        print("📂 File received:", file.filename)
        print("📁 Saved at:", filepath)
        print("Returning filename:", file.filename)   # 🔥 ADD HERE

        
        # 🔥 CLEAR OLD DATA
        retriever_store.clear()

        # 🔥 PROCESS NEW PDF
        retriever = process_pdf(filepath)
        retriever_store["default"] = retriever

        return jsonify({
            "message": "Upload successful",
            "filename": file.filename   # 🔥 ADD THIS LINE
            })
    except Exception as e:
        print("❌ Upload error:", str(e))
        return jsonify({"error": "Upload failed"}), 500

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        question = data.get("question")

        if "default" not in retriever_store:
            return jsonify({"answer": "⚠️ Please upload a PDF first"})

        retriever = retriever_store["default"]  # 🔥 always latest

        answer = ask_question(question, retriever)

        return jsonify({"answer": answer})

    except Exception as e:
        print("❌ Ask error:", str(e))
        return jsonify({"answer": "❌ Error generating answer"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)