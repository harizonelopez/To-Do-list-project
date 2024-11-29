// API Base URL for Flask
const apiUrl = "http://127.0.0.1:5000/api"; // Update this if deployed
// const apiUrl = `${window.location.origin}/api`; // Dynamically set base URL

// Elements
const container = document.getElementById("container");
const registerBtn = document.getElementById("register");
const loginBtn = document.getElementById("login");

// Toggle between sign-up and sign-in
if (registerBtn) {
    registerBtn.addEventListener("click", () => {
        container.classList.add("active");
    });
}


if (loginBtn) {
    loginBtn.addEventListener("click", () => {
        container.classList.remove("active");
    });
}


// Handle sign-in functionality
const loginForm = document.querySelector(".sign-in form");
if (loginForm) {
    loginForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent form submission
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (username && password) {
            // Fetch the user from Flask API
            fetch("/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({ 
                    username: document.getElementById("username").value, 
                    password: document.getElementById("password").value, 
                }),
            })
                .then((response) => {
                    if (response.redirected) {
                        window.location.href = response.url;
                    } else if (!response.ok) {
                        throw new Error("Invalid username or password")
                    }
                })
                .catch((error) => {
                    console.error("Login failed:", error);
                    alert("Invalid username or password. Try again."); // Show error
                });
        } else {
            alert("Please enter both username and password.");
        }
    });
}


// Handle sign-up functionality
const signUpUser = () => {
    const username = document.getElementById("sign-up-user").value.trim();
    const password = document.getElementById("sign-up-pass").value.trim();
    const confirmPassword = document.getElementById("sign-up-ConPass").value.trim();

    if (!username || !password || !confirmPassword) {
        alert("Please fill out all fields.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // Send the form data using the fetch API
    fetch("/api/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
            username: username,
            password: password,
        }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text(); // Flask renders HTML response
        })
        .then((html) => {
            document.body.innerHTML = html; // Render the returned HTML
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while creating the user.");
        });
};


const signUpBtn = document.getElementById("Up");
if (signUpBtn) {
    signUpBtn.addEventListener("click", signUpUser);
}

setTimeout(() => {
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.style.transition = "opacity 0.5s ease-out";
        flashMessages.style.opacity = 0; // Fade out
        setTimeout(() => flashMessages.remove(), 500); // Remove after fade-out
    }
}, 5000);