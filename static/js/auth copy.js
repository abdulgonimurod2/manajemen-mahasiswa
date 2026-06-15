const API_BASE_URL = "/api";

document.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname;
    const isLogin = path === "/" || path.includes("index.html");
    const token = sessionStorage.getItem("token");

    if (!isLogin && !token) {
        window.location.href = "/";
        return;
    }

    if (isLogin && token) {
        window.location.href = "dashboard.html";
        return;
    }

    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const alertBox = document.getElementById("loginAlert");

            try {
                const res = await fetch(`${API_BASE_URL}/auth/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });

                const data = await res.json();
                if (res.ok) {
                    sessionStorage.setItem("token", data.token);
                    sessionStorage.setItem("user", data.user);
                    window.location.href = "dashboard.html";
                } else {
                    alertBox.textContent = data.detail || "Login gagal";
                    alertBox.classList.remove("d-none");
                }
            } catch (err) {
                alertBox.textContent = "Terjadi kesalahan server";
                alertBox.classList.remove("d-none");
            }
        });
    }

    const btnLogout = document.getElementById("btnLogout");

    if (btnLogout) {
        btnLogout.addEventListener("click", async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/auth/logout`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });

                const data = await response.json();

                alert(data.message);

                sessionStorage.clear();

                window.location.href = "/";
            } catch (error) {
                console.error("Logout Error:", error);
                alert("Gagal logout");
            }
        });
    }
});
