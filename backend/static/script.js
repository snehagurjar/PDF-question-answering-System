document.addEventListener("DOMContentLoaded", function () {

  const chatBox = document.getElementById("chat-box");

  document.getElementById("pdfFile").addEventListener("change", function () {
    const file = this.files[0];
    document.getElementById("fileName").innerText =
      file ? "📄 " + file.name : "";
  });

  // 🔹 Upload
  window.uploadPDF = async function () {

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
    status.innerText = "⏳ Uploading...";

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/upload", {
        method: "POST",
        body: formData
      });

      const data = await res.json();

      status.innerText = `✅ ${data.filename} uploaded`;

      document.getElementById("askBtn").disabled = false;

      chatBox.innerHTML += `
        <div class="message bot">
          📄 ${data.filename} uploaded successfully!
        </div>
      `;

      uploadBtn.disabled = false;
      uploadBtn.innerText = "Upload PDF";

    } catch (err) {
      status.innerText = "❌ Upload failed";
      uploadBtn.disabled = false;
      uploadBtn.innerText = "Upload PDF";
    }
  };

  // 🔹 Ask
  window.askQuestion = async function () {

    const input = document.getElementById("question");
    const question = input.value.trim();

    if (!question) return;

    chatBox.innerHTML += `
      <div class="message user">${question}</div>
    `;

    input.value = "";

    const loadingId = "load-" + Date.now();

    chatBox.innerHTML += `
      <div id="${loadingId}">⏳ Thinking...</div>
    `;

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

});