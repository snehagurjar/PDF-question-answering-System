from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from rag_pipeline import process_pdf, ask_question

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

pdf_text_store = {}  # 🔥 store plain text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    try:
        global pdf_text_store

        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        print("📂 File received:", file.filename)

        # 🔥 clear old
        pdf_text_store.clear()

        # 🔥 process pdf
        text = process_pdf(filepath)
        pdf_text_store["data"] = text

        return jsonify({
            "message": "Upload successful",
            "filename": file.filename
        })

    except Exception as e:
        print("❌ Upload error:", str(e))
        return jsonify({"error": "Upload failed"}), 500


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        question = data.get("question")

        if "data" not in pdf_text_store:
            return jsonify({"answer": "⚠️ Please upload a PDF first"})

        text = pdf_text_store["data"]

        answer = ask_question(question, text)

        return jsonify({"answer": answer})

    except Exception as e:
        print("❌ Ask error:", str(e))
        return jsonify({"answer": "❌ Error generating answer"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)