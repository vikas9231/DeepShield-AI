document.getElementById("loginForm").addEventListener("submit", async function (e) {

    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    try {

        const response = await fetch("/api/login", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                email,
                password

            })

        });

        const result = await response.json();

        if (response.ok) {

            localStorage.setItem("isLoggedIn", "true");

            localStorage.setItem("currentUser", JSON.stringify(result.user));

            alert(result.message);

            window.location.href = "/dashboard";

        }

        else {

            alert(result.message);

        }

    }

    catch (error) {

        console.error(error);

        alert("Unable to connect to the server.");

    }

});