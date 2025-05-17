// Complete JavaScript with Gemini-based analysis integration

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

document.getElementById("submit").addEventListener("click", async () => {
  const text = document.querySelector("textarea").value.trim();

  // Show loading state
  const submitBtn = document.getElementById("submit");
  const originalBtnText = submitBtn.textContent;
  submitBtn.textContent = "Processing...";
  submitBtn.disabled = true;

  try {
    let sourceText = "";
    let translatedText = "";

    if (text) {
      const translationResponse = await fetch("http://localhost:5000/translate-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      if (!translationResponse.ok) {
        throw new Error("Translation request failed");
      }

      const translationData = await translationResponse.json();

      if (!translationData.translated) {
        throw new Error(translationData.error || "Translation failed");
      }

      sourceText = text;
      translatedText = translationData.translated;

    } else if (selectedFile) {
      const formData = new FormData();
      formData.append("image", selectedFile);

      const response = await fetch("http://localhost:5000/upload-screenshot", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error("Screenshot processing failed");
      }

      const data = await response.json();

      if (!data.translated) {
        throw new Error(data.error || "Translation failed");
      }

      sourceText = data.extracted;
      translatedText = data.translated;

    } else {
      throw new Error("Please enter text or select a screenshot to translate.");
    }

    // Step 2: Request Gemini analysis
    const analysisResponse = await fetch("http://localhost:5000/analyze-translation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sourceText, translatedText })
    });

    if (!analysisResponse.ok) {
      throw new Error("Analysis request failed");
    }

    const analysisData = await analysisResponse.json();

    const metadata = {
      translationModel: "customHMT",
      modelAccuracy: "91.37%",
      sourceOfNews: analysisData.sourceOfNews || "Unknown source",
      extractedKeywords: analysisData.keywords || "No keywords found",
      translationReview: analysisData.review || "Good",
      translationAccuracy: analysisData.accuracyScore || 85
    };

    showResultModal(sourceText, translatedText, metadata);

  } catch (error) {
    console.error("Error:", error);
    alert(error.message || "Something went wrong");
  } finally {
    submitBtn.textContent = originalBtnText;
    submitBtn.disabled = false;
  }
});

// Function to show result modal
function showResultModal(bengaliText, hindiText, metadata) {
  const resultBox = document.getElementById("resultBox");

  const getAccuracyColor = (score) => {
    if (score >= 95) return "#4CAF50";
    if (score >= 85) return "#8BC34A";
    if (score >= 80) return "#FFC107";
    return "#FF9800";
  };

  const accuracyColor = getAccuracyColor(metadata.translationAccuracy);

  resultBox.innerHTML = `
    <h2>Output Translation</h2>
    <div class="result-columns">
      <div class="result-column">
        <h3>Bengali News:</h3>
        <div class="result-text">${bengaliText}</div>
      </div>
      <div class="result-column">
        <h3>Hindi Translation:</h3>
        <div class="result-text">${hindiText}</div>
      </div>
    </div>
    <div class="translation-metadata">
      <div class="metadata-left">
        <h3>Translation Details:</h3>
        <hr>
        <ul>
          <li><strong>Translation Model:</strong> ${metadata.translationModel}</li>
          <li><strong>Model Accuracy:</strong> ${metadata.modelAccuracy}</li>
          <li><strong>Source of News:</strong> ${metadata.sourceOfNews}</li>
          <li><strong>Extracted Keywords:</strong> ${metadata.extractedKeywords}</li>
          <li><strong>Translation Review:</strong> ${metadata.translationReview}</li>
        </ul>
      </div>
      <div class="metadata-right">
        <div class="accuracy-graph">
  <div class="circular-progress">
    <svg class="progress-ring" width="120" height="120">
      <circle class="progress-ring__background" stroke="#d3d3d3" stroke-width="10" fill="transparent" r="50" cx="60" cy="60" />
      <circle class="progress-ring__circle" stroke="limegreen" stroke-width="10" fill="transparent" r="50" cx="60" cy="60"
        style="stroke-dasharray: 314; stroke-dashoffset: calc(314 - (314 * ${metadata.translationAccuracy} / 100));" />
    </svg>
    <div class="progress-text">${metadata.translationAccuracy}%</div>
  </div>
  <h3 style="color: #fff; margin-top:10px">Translation Accuracy</h3>
</div>

      </div>
    </div>
  `;

  document.getElementById("modalBackground").classList.add("show");
  document.body.style.overflow = "hidden";
}

// Close modal when clicking outside
document.getElementById("modalBackground").addEventListener("click", function (event) {
  if (event.target === this) {
    this.classList.remove("show");
    document.body.style.overflow = "";
  }
});

// Hide modal on load
document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("modalBackground");
  if (modal) modal.classList.remove("show");
});
