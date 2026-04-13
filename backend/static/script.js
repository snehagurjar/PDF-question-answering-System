document.addEventListener("DOMContentLoaded", function () {

  let chatBox = document.getElementById("chat-box");

  // 🔹 Show selected file name
  document.getElementById("pdfFile").addEventListener("change", function () {
    const file = this.files[0];
    document.getElementById("fileName").innerText = file ? "📄 " + file.name : "";
  });

  // 🔹 Upload PDF
  window.uploadPDF = async function () {
    alert("Upload clicked");

    const fileInput = document.getElementById("pdfFile");
    const file = fileInput.files[0];
    const status = document.getElementById("uploadStatus");
    const uploadBtn = document.querySelector(".upload button");

    if (!file) {
      status.innerText = "⚠️ Please select a file first";
      return;
    }

    uploadBtn.disabled = true;
    uploadBtn.innerText = "Uploading...";
    status.innerText = "⏳ Uploading PDF...";

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/upload", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      const filename = data.filename || "PDF";

      status.innerHTML = `✅ ${filename} uploaded successfully!`;

      document.getElementById("askBtn").disabled = false;

      if (chatBox) {
        chatBox.innerHTML += `
          <div class="message bot">
            📄 <b>${filename}</b> uploaded successfully!
          </div>
        `;
      }

      uploadBtn.disabled = false;
      uploadBtn.innerText = "Upload PDF";

    } catch (err) {
      status.innerText = "❌ Upload failed";
    }
  };

  // 🔹 Ask Question
  window.askQuestion = async function () {
    const input = document.getElementById("question");
    const question = input.value.trim();

    if (!question) return;

    if (chatBox) {
      chatBox.innerHTML += `<div class="message user">${question}</div>`;
    }

    const loadingId = "loading-" + Date.now();

    if (chatBox) {
      chatBox.innerHTML += `<div id="${loadingId}">⏳ Thinking...</div>`;
    }

    try {
      const res = await fetch("/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
      });

      const data = await res.json();

      document.getElementById(loadingId).innerHTML =
        (data.answer || "No answer").replace(/\n/g, "<br>");

    } catch (err) {
      document.getElementById(loadingId).innerText = "❌ Error";
    }
  };

  // 🔹 Enter key
  document.getElementById("question").addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
      askQuestion();
    }
  });

});