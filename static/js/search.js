document.addEventListener("DOMContentLoaded", () => {
    const btnSearch = document.getElementById("btnSearch");
    if (btnSearch) {
        btnSearch.addEventListener("click", async () => {
            const query = document.getElementById("searchInput").value;
            const method = document.getElementById("searchMethod").value;
            const field = document.getElementById("searchField").value;

            // UX Enhancement for visual loading
            const orig = btnSearch.innerHTML;
            btnSearch.innerHTML = `<span class="spinner-border spinner-border-sm" role="status"></span>`;

            if (!query) {
                // If empty search box, essentially get all.
                try {
                    const res = await fetch(`/api/mahasiswa`);
                    const json = await res.json();
                    if (res.ok) {
                        dataMahasiswa = json.data;
                        currentPage = 1;
                        renderTable();
                        updateExecInfo("GET /api/mahasiswa", json.execution_time_ms, "ALL", "Reset pencarian ke status mula-mula");
                    }
                } catch (e) { }
                btnSearch.innerHTML = orig;
                return;
            }

            try {
                const res = await fetch(`/api/mahasiswa/search?query=${encodeURIComponent(query)}&method=${method}&field=${field}`);
                const json = await res.json();

                if (res.ok) {
                    currentPage = 1;
                    dataMahasiswa = json.data;
                    renderTable();
                    let hint = "O(n)";
                    if (method === 'binary') hint = "O(log n) (Binary Split)";
                    updateExecInfo("/api/mahasiswa/search", json.execution_time_ms, method.toUpperCase(), hint);
                } else {
                    showToast("Error Pencarian", json.detail, "danger");
                }
            } catch (err) {
                showToast("Error", err.message, "danger");
            }
            btnSearch.innerHTML = orig;
        });
    }
});
