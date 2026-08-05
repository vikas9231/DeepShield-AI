// ==========================================
// Elements
// ==========================================

const profileName = document.getElementById("profileName");
const profileEmail = document.getElementById("profileEmail");

const fullName = document.getElementById("fullName");
const email = document.getElementById("email");
const phone = document.getElementById("phone");

const saveBtn = document.querySelector(".analyze-btn");

// ==========================================
// Load Profile
// ==========================================

async function loadProfile() {

    try {

        const response = await fetch(

            `/api/profile/${currentUser.id}`

        );

        const data = await response.json();

        if (!data.success) {

            alert(data.message);

            return;

        }

        const user = data.user;

        profileName.textContent = user.name;

        profileEmail.textContent = user.email;

        fullName.value = user.name;

        email.value = user.email;

        phone.value = user.phone || "";

    }

    catch (error) {

        console.error(error);

        alert("Unable to load profile.");

    }

}

// ==========================================
// Save Profile
// ==========================================

saveBtn.addEventListener("click", async function (e) {

    e.preventDefault();

    try {

        const response = await fetch(

            `/api/profile/${currentUser.id}`,

            {

                method: "PUT",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    name: fullName.value,

                    phone: phone.value

                })

            }

        );

        const result = await response.json();

        alert(result.message);

        if (result.success) {

            currentUser.name = fullName.value;

            currentUser.phone = phone.value;

            localStorage.setItem(

                "currentUser",

                JSON.stringify(currentUser)

            );

            document.getElementById("username").textContent =
                currentUser.name;

            profileName.textContent =
                currentUser.name;

        }

    }

    catch (error) {

        console.error(error);

        alert("Unable to update profile.");

    }

});

// ==========================================
// Load
// ==========================================

loadProfile();

// ==========================================
// Load Statistics
// ==========================================

async function loadStats() {

    try {

        const response = await fetch(

            `/api/dashboard/${currentUser.id}`

        );

        const data = await response.json();

        if (!data.success) return;

        document.getElementById("profileTotalScans").textContent =
            data.total_scans;

        document.getElementById("profileImages").textContent =
            data.images;

        document.getElementById("profileVideos").textContent =
            data.videos;

        document.getElementById("profileReports").textContent =
            data.reports;

    }

    catch (error) {

        console.error(error);

    }

}

loadStats();