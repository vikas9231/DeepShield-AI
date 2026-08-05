// ==========================================
// Elements
// ==========================================

const darkMode = document.getElementById("darkMode");
const emailNotifications = document.getElementById("emailNotifications");
const detectionAlerts = document.getElementById("detectionAlerts");
const language = document.getElementById("language");

const currentPassword = document.getElementById("currentPassword");
const newPassword = document.getElementById("newPassword");
const confirmPassword = document.getElementById("confirmPassword");

const saveSettings = document.getElementById("saveSettings");
const changePassword = document.getElementById("changePassword");

// ==========================================
// Load Settings
// ==========================================

async function loadSettings() {

    try {

        const response = await fetch(

            `/api/settings/${currentUser.id}`

        );

        const data = await response.json();

        if (!data.success) return;

        darkMode.checked =
            data.settings.dark_mode;

        emailNotifications.checked =
            data.settings.email_notifications;

        detectionAlerts.checked =
            data.settings.detection_alerts;

        language.value =
            data.settings.language;

    }

    catch (error) {

        console.error(error);

    }

}

// ==========================================
// Save Settings
// ==========================================

saveSettings.addEventListener("click", async function (e) {

    e.preventDefault();

    try {

        const response = await fetch(

            `/api/settings/${currentUser.id}`,

            {

                method: "PUT",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    dark_mode: darkMode.checked,

                    email_notifications: emailNotifications.checked,

                    detection_alerts: detectionAlerts.checked,

                    language: language.value

                })

            }

        );

        const result = await response.json();

        alert(result.message);

    }

    catch (error) {

        console.error(error);

    }

});

// ==========================================
// Change Password
// ==========================================

changePassword.addEventListener("click", async function (e) {

    e.preventDefault();

    if (newPassword.value !== confirmPassword.value) {

        alert("Passwords do not match.");

        return;

    }

    try {

        const response = await fetch(

            "/api/change-password",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    user_id: currentUser.id,

                    current_password: currentPassword.value,

                    new_password: newPassword.value

                })

            }

        );

        const result = await response.json();

        alert(result.message);

        if (result.success) {

            currentPassword.value = "";
            newPassword.value = "";
            confirmPassword.value = "";

        }

    }

    catch (error) {

        console.error(error);

    }

});

// ==========================================
// Load
// ==========================================

loadSettings();