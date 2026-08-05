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
// Future Report Logic
// ==========================================

// Report data, PDF download and print functionality
// will be added in the next phase.