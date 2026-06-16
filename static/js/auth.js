const API_BASE_URL = "/api";

document.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname;
    const isLoginPage = path === "/" || path.includes("index.html");
    const token = sessionStorage.getItem("token");

    const loginAlert = document.getElementById("loginAlert");

    // show alert
    function showAlert(message, type = "danger") {
        if (!loginAlert) return;

        loginAlert.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <strong>${type === "success" ? "Berhasil!" : "Perhatian!"}</strong>
                ${message}
                <button
                    type="button"
                    class="btn-close"
                    data-bs-dismiss="alert"
                    aria-label="Close">
                </button>
            </div>
        `;

        loginAlert.classList.remove("d-none");
    }

    const successMessage = sessionStorage.getItem("successMessage");
    if (successMessage && loginAlert) {
        showAlert(successMessage, "success");
        sessionStorage.removeItem("successMessage");
    }

    if (!isLoginPage && !token) {
        window.location.href = "/";
        return;
    }

    if (isLoginPage && token) {
        window.location.href = "/dashboard.html";
        return;
    }

    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", handleLogin);
    }

    const btnLogout = document.getElementById("btnLogout");

    if (btnLogout) {
        btnLogout.addEventListener("click", handleLogout);
    }

    async function handleLogin(e) {
        e.preventDefault();

        const username = document
            .getElementById("username")
            .value
            .trim();

        const password = document
            .getElementById("password")
            .value
            .trim();

        try {
            const response = await fetch(
                `${API_BASE_URL}/auth/login`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        username,
                        password
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                showAlert(
                    data.detail || "Login gagal",
                    "danger"
                );
                return;
            }

            sessionStorage.setItem("token", data.token);
            sessionStorage.setItem(
                "user",
                JSON.stringify(data.user)
            );

            window.location.href = "/dashboard.html";

        } catch (error) {
            console.error(error);
            showAlert(
                "Terjadi kesalahan server",
                "danger"
            );
        }
    }

    async function handleLogout() {
        try {
            const response = await fetch(
                `${API_BASE_URL}/auth/logout`,
                {
                    method: "POST"
                }
            );

            const data = await response.json();

            sessionStorage.clear();

            sessionStorage.setItem(
                "successMessage",
                data.message || "Logout berhasil"
            );

            window.location.href = "/";

        } catch (error) {
            console.error(error);

            sessionStorage.clear();

            sessionStorage.setItem(
                "successMessage",
                "Logout berhasil"
            );

            window.location.href = "/";
        }
    }
});