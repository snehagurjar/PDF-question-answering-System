
const BASE_URL = "https://pdf-question-answering-system.onrender.com";
// const chatBox = document.getElementById("chat-box");
let chatBox;

window.onload = function () {
  chatBox = document.getElementById("chat-box");
};


document.getElementById("pdfFile").addEventListener("change", function () {
  const file = this.files[0];
  document.getElementById("fileName").innerText = file ? "📄 " + file.name : "";
});


async function uploadPDF() {
  const fileInput = document.getElementById("pdfFile");
  const file = fileInput.files[0];
  const status = document.getElementById("uploadStatus");
  const uploadBtn = document.querySelector(".upload button");

  if (!file) {
    status.innerText = "⚠️ Please select a file first";
    return;
  }

  // 🔥 Uploading state
  uploadBtn.disabled = true;
  uploadBtn.innerText = "Uploading...";
  status.innerText = "⏳ Uploading PDF...";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      throw new Error("Upload failed");
    }

    const data = await res.json();

    const filename = data.filename || "PDF";

    // 🔥 CLEAR previous status
    status.innerHTML = "";

    // 🔥 CREATE NEW UI ELEMENT (guaranteed render)
    const successBox = document.createElement("div");
    successBox.style.background = "#d4edda";
    successBox.style.color = "#155724";
    successBox.style.padding = "12px";
    successBox.style.borderRadius = "8px";
    successBox.style.marginTop = "10px";
    successBox.style.fontWeight = "bold";

    successBox.innerHTML = `
      ✅ File Uploaded Successfully! <br>
      📄 ${filename}
    `;

    // 🔥 ADD TO UI
    status.appendChild(successBox);

    // 🔥 ENABLE ASK BUTTON
    const askBtn = document.getElementById("askBtn");
    askBtn.disabled = false;

    // 🔥 SHOW IN CHAT ALSO (backup)
    chatBox.innerHTML += `
      <div class="message bot">
        📄 <b>${filename}</b> uploaded successfully!<br>
        👉 Now you can ask questions.
      </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    // 🔥 RESET upload button
    uploadBtn.disabled = false;
    uploadBtn.innerText = "Upload PDF";

    // clear file input
    fileInput.value = "";

  } catch (err) {
    console.error("Upload Error:", err);

    status.innerHTML = `
      <div style="color:red; font-weight:bold;">
        ❌ Upload failed. Try again.
      </div>
    `;

    uploadBtn.disabled = false;
    uploadBtn.innerText = "Upload PDF";
  }
}
// 🔹 Ask Question
async function askQuestion() {
  const input = document.getElementById("question");
  const question = input.value.trim();

  if (!question) return;

  // 👤 user message
  chatBox.innerHTML += `
    <div class="message user">${question}</div>
  `;

  input.value = "";

  // 🤖 loading
  const loadingId = "loading-" + Date.now();
  chatBox.innerHTML += `
    <div class="message bot" id="${loadingId}">⏳ Thinking...</div>
  `;

  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch(`${BASE_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    const data = await res.json();

    let answer;

    if (data.error) {
      answer = "⚠️ " + data.error;
    } else {
      answer = data.answer || "⚠️ No answer found";
    }

    // format
    answer = answer.replace(/\n/g, "<br>");

    document.getElementById(loadingId).innerHTML = answer;

    chatBox.scrollTop = chatBox.scrollHeight;

  } catch (err) {
    console.error("Ask Error:", err);
    document.getElementById(loadingId).innerText = "❌ Server error";
  }
}


// 🔹 Enter key support
document.getElementById("question").addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    askQuestion();
  }
});