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

    document.getElementById("profileName").textContent = currentUser.name;

    document.getElementById("profileEmail").textContent = currentUser.email;

    document.getElementById("fullName").value = currentUser.name;

    document.getElementById("email").value = currentUser.email;

    document.getElementById("phone").value = currentUser.phone || "";

}

// ==========================================
// Load Profile Statistics
// ==========================================

async function loadProfileStats() {

    try {

        const response = await fetch(`/api/dashboard/${currentUser.id}`);

        const data = await response.json();

        if (!data.success) return;

        document.getElementById("profileTotalScans").textContent = data.total_scans;

        document.getElementById("profileImages").textContent = data.images;

        document.getElementById("profileVideos").textContent = data.videos;

        document.getElementById("profileReports").textContent = data.reports;

    }

    catch (error) {

        console.error(error);

    }

}

loadProfileStats();