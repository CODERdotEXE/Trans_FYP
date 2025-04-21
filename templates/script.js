const fileInput = document.getElementById("fileInput");
const selectBtn = document.getElementById("selectBtn");
const previewBox = document.getElementById("previewBox");

let selectedFile = null;

// When "Select Screenshot" is clicked
selectBtn.addEventListener("click", () => {
  fileInput.click();
});

// Show preview when a file is selected
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = () => {
      previewBox.innerHTML = `
        <img src="${reader.result}" />
        <button class="remove-btn" onclick="removeImage()">❌</button>
      `;
      selectBtn.style.display = "none";
    };
    reader.readAsDataURL(file);
  }
});

// Reset preview and file
function removeImage() {
  selectedFile = null;
  fileInput.value = "";
  previewBox.innerHTML = "";
  selectBtn.style.display = "inline-block";
}

// Translate button handles both text or screenshot
document.getElementById("submit").addEventListener("click", async () => {
  const text = document.querySelector("textarea").value.trim();

  if (text) {
    // Text translation
    try {
      const response = await fetch("http://localhost:5000/translate-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();
      alert("Translated Text:\n\n" + data.translated);
    } catch (error) {
      console.error("Text translation failed:", error);
      alert("Something went wrong.");
    }
  } else if (selectedFile) {
    // Image translation
    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch("http://localhost:5000/upload-screenshot", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (data.translated) {
        alert("Screenshot Translated Text:\n\n" + data.translated);
      } else {
        alert("Error: " + (data.error || "Unknown error"));
      }
    } catch (error) {
      console.error("Screenshot translation failed:", error);
      alert("Something went wrong.");
    }
  } else {
    alert("Please enter text or select a screenshot to translate.");
  }
});


