const email = sessionStorage.getItem("resetEmail");

if (!email) {
    window.location.href = "/forgot-password";
}

document.getElementById("resetForm").addEventListener("submit", async function (e) {

    e.preventDefault();

    const password = document.getElementById("password").value;
    const confirm = document.getElementById("confirmPassword").value;

    if (password !== confirm) {
        alert("Passwords do not match.");
        return;
    }

    try {

        console.log("Email:", email);
        console.log("Password:", password);

        const response = await fetch("/api/reset-password", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email,
                password
            })

        });

        console.log("Status:", response.status);

        const result = await response.json();

        console.log(result);

        alert(result.message);

        if (response.ok) {

            sessionStorage.removeItem("resetEmail");

            window.location.href = "/login";

        }

    }
    catch (error) {

        console.error(error);

        alert("Something went wrong.");

    }

});