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

if (currentUser && document.getElementById("username")) {

    document.getElementById("username").textContent = currentUser.name;

}

// ==========================================
// Logout
// ==========================================

function logout() {

    if (!confirm("Are you sure you want to logout?")) {

        return;

    }

    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("currentUser");

    window.location.href = "/";

}

// ==========================================
// Dashboard Only
// ==========================================

const totalScans = document.getElementById("totalScans");
const totalImages = document.getElementById("totalImages");
const totalVideos = document.getElementById("totalVideos");
const totalDeepfakes = document.getElementById("totalDeepfakes");
const accuracy = document.getElementById("accuracy");
const totalReports = document.getElementById("totalReports");
const recentTable = document.getElementById("recentTable");

// ==========================================
// Load Dashboard Statistics
// ==========================================

async function loadDashboard() {

    try {

        const response = await fetch(`/api/dashboard/${currentUser.id}`);

        if (!response.ok) {

            throw new Error(`HTTP ${response.status}`);

        }

        const data = await response.json();

        if (!data.success) {

            alert(data.message || "Unable to load dashboard.");

            return;

        }

        totalScans.textContent = data.total_scans;
        totalImages.textContent = data.images;
        totalVideos.textContent = data.videos;
        totalDeepfakes.textContent = data.deepfakes;
        accuracy.textContent = data.accuracy + "%";
        totalReports.textContent = data.reports;

    }

    catch (error) {

        console.error("Dashboard Error:", error);

    }

}

// ==========================================
// Load Recent Activity
// ==========================================

async function loadRecentActivity() {

    if (!recentTable) return;

    try {

        const response = await fetch(`/api/dashboard/recent/${currentUser.id}`);

        const result = await response.json();

        recentTable.innerHTML = "";

        if (!result.success || result.recent.length === 0) {

            recentTable.innerHTML = `
                <tr>
                    <td colspan="4">No recent activity found.</td>
                </tr>
            `;

            return;

        }

        result.recent.forEach(scan => {

            const badge = scan.prediction === "Real"
                ? "✅ Real"
                : "⚠ Deepfake";

            recentTable.innerHTML += `
                <tr>
                    <td>${scan.date}</td>
                    <td>${scan.filename}</td>
                    <td>${badge}</td>
                    <td>${scan.confidence}%</td>
                </tr>
            `;

        });

    }

    catch (error) {

        console.error(error);

    }

}

// ==========================================
// Execute Only on Dashboard Page
// ==========================================

if (totalScans) {

    loadDashboard();

}

if (recentTable) {

    loadRecentActivity();

}