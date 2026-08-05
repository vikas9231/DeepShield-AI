document
.getElementById("forgotForm")
.addEventListener("submit", async function(e){

    e.preventDefault();

    const email =
        document.getElementById("forgotEmail").value.trim();

    const response = await fetch("/api/forgot-password",{

        method:"POST",

        headers:{

            "Content-Type":"application/json"

        },

        body:JSON.stringify({

            email

        })

    });

    const result = await response.json();

    if(response.ok){

        sessionStorage.setItem("resetEmail",email);

        window.location.href="/reset-password";

    }

    else{

        alert(result.message);

    }

});