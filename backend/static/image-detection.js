// ==========================================
// Login Check
// ==========================================

console.log("Image Detection JS Loaded");

if (localStorage.getItem("isLoggedIn") !== "true") {

    window.location.href = "/login";

}

// ==========================================
// Current User
// ==========================================

// const currentUser = JSON.parse(localStorage.getItem("currentUser"));

if (currentUser) {

    document.getElementById("username").textContent = currentUser.name;

}

// ==========================================
// Elements
// ==========================================

const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const dropArea = document.getElementById("dropArea");

const analyzeBtn = document.getElementById("analyzeBtn");

const statusText = document.getElementById("statusText");
const confidenceText = document.getElementById("confidenceText");
const fakeText = document.getElementById("fakeText");
const realText = document.getElementById("realText");

let selectedImage = null;

// ==========================================
// Browse Image
// ==========================================

imageInput.addEventListener("change", function () {

    console.log("Image Selected");

    console.log(this.files);

    if (this.files.length > 0) {

        console.log("Calling loadImage()");

        loadImage(this.files[0]);

    }

});

// ==========================================
// Drag & Drop
// ==========================================

dropArea.addEventListener("dragover", function (e) {

    e.preventDefault();

    dropArea.style.borderColor = "#00d4ff";

});

dropArea.addEventListener("dragleave", function () {

    dropArea.style.borderColor = "#3b82f6";

});

dropArea.addEventListener("drop", function (e) {

    e.preventDefault();

    dropArea.style.borderColor = "#3b82f6";

    if (e.dataTransfer.files.length > 0) {

        loadImage(e.dataTransfer.files[0]);

    }

});

// ==========================================
// Load Image
// ==========================================

function loadImage(file) {
    console.log("Inside loadImage()");
    console.log(file);

    if (!file.type.startsWith("image/")) {

        alert("Please select an image.");

        return;

    }

    if (file.size > 10 * 1024 * 1024) {

        alert("Maximum image size is 10 MB.");

        return;

    }

    selectedImage = file;

    const reader = new FileReader();

    reader.onload = function (e) {

        previewImage.src = e.target.result;

        previewImage.style.display = "block";

        resetResult();

    };

    reader.readAsDataURL(file);

}

// ==========================================
// Reset Result
// ==========================================

function resetResult() {

    statusText.textContent = "Waiting for Analysis...";
    confidenceText.textContent = "0%";
    fakeText.textContent = "0%";
    realText.textContent = "0%";

    statusText.style.color = "";

}

// ==========================================
// Analyze Image
// ==========================================

analyzeBtn.addEventListener("click", async function (e) {

    e.preventDefault();

    if (!selectedImage) {

        alert("Please upload an image first.");

        return;

    }

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = "Analyzing...";

    try {

        const formData = new FormData();

        formData.append("image", selectedImage);
        formData.append("user_id", currentUser.id);

        const response = await fetch("/api/upload-image", {

            method: "POST",

            body: formData

        });

        const result = await response.json();

        if (!response.ok) {

            throw new Error(result.message);

        }

        statusText.innerHTML = result.prediction;
        confidenceText.innerHTML = result.confidence + "%";

        fakeText.innerHTML =
            (result.raw_prediction * 100).toFixed(2) + "%";

        realText.innerHTML =
            ((1 - result.raw_prediction) * 100).toFixed(2) + "%";

        if (result.prediction === "Deepfake") {

            statusText.style.color = "#ef4444";

        }

        else {

            statusText.style.color = "#22c55e";

        }

        statusText.innerHTML +=
            `<br><small>Risk: ${result.risk_level}</small>`;

    }

    catch (error) {

        console.error(error);

        alert(error.message || "Server Error");

    }

    finally {

        analyzeBtn.disabled = false;

        analyzeBtn.innerHTML = "Analyze Image";

    }

});