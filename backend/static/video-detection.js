// ==========================================
// Login Check
// ==========================================

if (localStorage.getItem("isLoggedIn") !== "true") {

    window.location.href = "/login";

}

document.getElementById("username").textContent = currentUser.name;

// ==========================================
// Elements
// ==========================================

const videoInput = document.getElementById("videoInput");
const videoPreview = document.getElementById("videoPreview");
const videoDropArea = document.getElementById("videoDropArea");

const analyzeVideo = document.getElementById("analyzeVideo");

const progressBar = document.getElementById("progressBar");

const videoStatus = document.getElementById("videoStatus");
const videoConfidence = document.getElementById("videoConfidence");
const videoFake = document.getElementById("videoFake");
const videoReal = document.getElementById("videoReal");

let selectedVideo = null;

// ==========================================
// Select Video
// ==========================================

videoInput.addEventListener("change", function () {

    if (this.files.length > 0) {

        loadVideo(this.files[0]);

    }

});

function loadVideo(file){

    if(!file.type.startsWith("video/")){

        alert("Please choose a video.");

        return;

    }

    selectedVideo = file;

    videoPreview.src = URL.createObjectURL(file);

    videoPreview.style.display = "block";

    document.getElementById("videoName").textContent = file.name;

    document.getElementById("videoSize").textContent =
        (file.size/(1024*1024)).toFixed(2)+" MB";

    document.getElementById("videoFormat").textContent =
        file.type;

    videoPreview.onloadedmetadata=function(){

        document.getElementById("videoDuration").textContent =
            Math.floor(videoPreview.duration)+" sec";

    };

}

// ==========================================
// Analyze Video
// ==========================================

analyzeVideo.addEventListener("click", async function () {

    if (!selectedVideo) {

        alert("Please upload a video first.");

        return;

    }

    analyzeVideo.disabled = true;

    analyzeVideo.innerHTML = "Analyzing...";

    progressBar.style.width = "20%";

    try {

        const formData = new FormData();

        formData.append("video", selectedVideo);

        formData.append("user_id", currentUser.id);

        const response = await fetch("/api/upload-video", {

            method: "POST",

            body: formData

        });

        progressBar.style.width = "80%";

        const result = await response.json();

        if (!response.ok) {

            throw new Error(result.message);

        }

        progressBar.style.width = "100%";

        videoStatus.innerHTML = result.prediction;

        videoConfidence.innerHTML = result.confidence + "%";

        videoFake.innerHTML =
            (result.raw_prediction * 100).toFixed(2) + "%";

        videoReal.innerHTML =
            ((1 - result.raw_prediction) * 100).toFixed(2) + "%";

        if (result.prediction === "Deepfake") {

            videoStatus.style.color = "#ef4444";

        }

        else {

            videoStatus.style.color = "#22c55e";

        }

        videoStatus.innerHTML +=
            `<br><small>Risk: ${result.risk_level}</small>`;

    }

    catch (error) {

        console.error(error);

        alert(error.message || "Server Error");

    }

    finally {

        analyzeVideo.disabled = false;

        analyzeVideo.innerHTML = "Analyze Video";

    }

});