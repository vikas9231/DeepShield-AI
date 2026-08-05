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
// Future Settings Logic
// ==========================================

// In the next phase we'll add:
//
// ✓ Change Password
// ✓ Dark Mode
// ✓ Email Notifications
// ✓ Language Preferences
// ✓ Detection Alerts
//
// and store them in the database.