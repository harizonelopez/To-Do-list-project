// API Base URL for Flask
const apiUrl = "http://127.0.0.1:5000/api"; // Update this if deployed

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
            fetch(`${apiUrl}/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Invalid username or password");
                    }
                    return response.json();
                })
                .then((user) => {
                    // Successful login, store userID in localStorage
                    localStorage.setItem("userID", user.userID);
                    console.log("Login successful:", user);
                    window.location.href = "home_page.html"; // Redirect to home page
                })
                .catch((error) => {
                    console.error("Error during login:", error);
                    alert("Invalid username or password. Please try again."); // Show error
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

    /*const userData = {
        username,
        password,
    };*/

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
            return response.json();
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
