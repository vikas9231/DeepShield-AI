// ==========================================
// Elements
// ==========================================

const prediction = document.getElementById("reportPrediction");
const confidence = document.getElementById("reportConfidence");
const risk = document.getElementById("reportRisk");

const filename = document.getElementById("reportFilename");
const type = document.getElementById("reportType");
const resolution = document.getElementById("reportResolution");
const model = document.getElementById("reportModel");
const date = document.getElementById("reportDate");

const reportImage = document.getElementById("reportImage");
const imagePlaceholder = document.getElementById("imagePlaceholder");

const processingTime = document.getElementById("processingTime");

// ==========================================
// Load Latest Report
// ==========================================

async function loadReport() {

    try {

        const start = performance.now();

        const response = await fetch(`/api/report/${currentUser.id}`);

        const data = await response.json();

        if (!response.ok || !data.success) {

            alert(data.message || "Unable to load report.");

            return;

        }

        const report = data.report;

        // Prediction
        prediction.innerHTML =
            report.prediction === "Real"
                ? "✅ Real"
                : "⚠ Deepfake";

        prediction.style.color =
            report.prediction === "Real"
                ? "#22c55e"
                : "#ef4444";

        // Confidence
        confidence.textContent = report.confidence + "%";

        // Risk
        risk.textContent = report.risk_level;

        // File Details
        filename.textContent = report.filename;
        type.textContent = report.type;
        resolution.textContent = report.resolution || "-";
        model.textContent = report.model;
        date.textContent = report.date;

        // Preview
        if (report.type === "Image") {

            reportImage.src = "/uploads/" + report.filename;

            reportImage.style.display = "block";

            imagePlaceholder.style.display = "none";

        }

        else {

            reportImage.style.display = "none";

            imagePlaceholder.innerHTML = "Video Preview Not Available";

        }

        // Processing Time
        const end = performance.now();

        processingTime.textContent =
            ((end - start) / 1000).toFixed(2) + " sec";

    }

    catch (error) {

        console.error("Report Error:", error);

        alert("Unable to load report.");

    }

}

// ==========================================
// Download Report
// ==========================================

document.getElementById("downloadPDF").addEventListener("click", function () {

    window.print();

});

// ==========================================
// Print Report
// ==========================================

document.getElementById("printReport").addEventListener("click", function () {

    window.print();

});

// ==========================================
// Initial Load
// ==========================================

loadReport();