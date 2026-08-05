// ==========================================
// Login Check
// ==========================================

if (localStorage.getItem("isLoggedIn") !== "true") {

    window.location.href = "/login";

}

// ==========================================
// Current User
// ==========================================

const currentUser = JSON.parse(localStorage.getItem("currentUser"));

if (currentUser) {

    document.getElementById("username").textContent = currentUser.name;

}

// ==========================================
// Elements
// ==========================================

const videoInput = document.getElementById("videoInput");
const videoPreview = document.getElementById("videoPreview");
const videoDropArea = document.getElementById("videoDropArea");
const progressBar = document.getElementById("progressBar");
const analyzeVideo = document.getElementById("analyzeVideo");

// ==========================================
// Browse Video
// ==========================================

videoInput.addEventListener("change", function () {

    if (this.files.length > 0) {

        loadVideo(this.files[0]);

    }

});

// ==========================================
// Drag & Drop
// ==========================================

videoDropArea.addEventListener("dragover", function (e) {

    e.preventDefault();

    videoDropArea.style.borderColor = "#22c55e";

});

videoDropArea.addEventListener("dragleave", function () {

    videoDropArea.style.borderColor = "#3b82f6";

});

videoDropArea.addEventListener("drop", function (e) {

    e.preventDefault();

    videoDropArea.style.borderColor = "#3b82f6";

    if (e.dataTransfer.files.length > 0) {

        loadVideo(e.dataTransfer.files[0]);

    }

});

// ==========================================
// Load Video
// ==========================================

function loadVideo(file) {

    if (!file.type.startsWith("video/")) {

        alert("Please select a video.");

        return;

    }

    if (file.size > 100 * 1024 * 1024) {

        alert("Maximum video size is 100 MB.");

        return;

    }

    videoPreview.src = URL.createObjectURL(file);

    videoPreview.style.display = "block";

    document.getElementById("videoName").textContent = file.name;
    document.getElementById("videoSize").textContent = (file.size / (1024 * 1024)).toFixed(2) + " MB";
    document.getElementById("videoFormat").textContent = file.type;

    videoPreview.onloadedmetadata = function () {

        document.getElementById("videoDuration").textContent =
            Math.floor(videoPreview.duration) + " sec";

    };

}

// ==========================================
// Analyze (Demo)
// ==========================================

analyzeVideo.addEventListener("click", function () {

    if (videoPreview.src === "") {

        alert("Please upload a video first.");

        return;

    }

    analyzeVideo.disabled = true;
    analyzeVideo.innerHTML = "Analyzing...";

    let progress = 0;

    progressBar.style.width = "0%";

    const interval = setInterval(function () {

        progress += 5;

        progressBar.style.width = progress + "%";

        if (progress >= 100) {

            clearInterval(interval);

            showResult();

        }

    }, 120);

});

// ==========================================
// Demo Result
// ==========================================

function showResult() {

    const confidence = (95 + Math.random() * 5).toFixed(2);

    const fake = Math.floor(Math.random() * 40);

    const real = 100 - fake;

    document.getElementById("videoStatus").innerHTML =
        fake > 50 ? "⚠ Deepfake" : "✅ Authentic";

    document.getElementById("videoConfidence").innerHTML =
        confidence + "%";

    document.getElementById("videoFake").innerHTML =
        fake + "%";

    document.getElementById("videoReal").innerHTML =
        real + "%";

    analyzeVideo.innerHTML = "Analyze Again";

    analyzeVideo.disabled = false;

}