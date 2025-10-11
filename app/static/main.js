// Live image preview -- register and login pages
const fileInput = document.getElementById("file");
const previewImg = document.getElementById("preview");

if (fileInput && previewImg) {
    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        if (file) {
            previewImg.src = URL.createObjectURL(file);
            previewImg.style.display = "block";
        } else {
            previewImg.src = "";
            previewImg.style.dispaly = "none";
        }
    });
}

// handle register
const registerForm = document.getElementById("registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const fileInput = document.getElementById("file");
        const file = fileInput.files[0];
        const responseText = document.getElementById("response");

        if (!file) {
            responseText.textContent = "Please select an image file.";
            return;
        }

        const formData = new FormData();
        formData.append("email", email);
        formData.append("file", file);

        responseText.textContent = "Registering...";

        try {
            const res = await fetch("/api/auth/register", {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if (res.ok) {
                responseText.textContent = "✅ " + data.message;
                responseText.style.color = "lightgreen";
            } else {
                responseText.textContent = "❌ " + (data.error || "Registration failed");
                responseText.style.color = "tomato";
            }
        } catch (err) {
            console.error(err)
            responseText.textContent = "Network error."
        }
    });
}
// handle login
const loginForm = document.getElementById("loginForm");
if(loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const fileInput = document.getElementById("file");
        const file = fileInput.files[0];
        const responseText = document.getElementById("response");

        if (!file) {
            responseText.textContent = "Please select an image file.";
            return;
        }

        const formData = new FormData();
        formData.append("email", email);
        formData.append("file", file);

        responseText.textContent = "Logging in..."

        try {
            const res = await fetch("/api/auth/login", {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if (res.ok) {
                responseText.textContent = "✅ " + data.message;
                responseText.style.color = "lightgreen";
                console.log("Access Token:", data.access_token);
            } else {
                responseText.textContent = "❌ " + (data.error || "Login failed");
                responseText.style.color = "tomato";
            }
        } catch (err) {
            console.error(err);
            responseText.textContent = "Network error."
        }
    });
}