document.addEventListener("DOMContentLoaded", () => {
    let currentSortOrder = "asc";

    document.querySelectorAll(".sortable").forEach(el => {
        el.addEventListener("click", async () => {
            const field = el.getAttribute("data-field");
            const method = document.getElementById("sortMethod").value;
            currentSortOrder = currentSortOrder === "asc" ? "desc" : "asc";

            try {
                const res = await fetch(`/api/mahasiswa/sort?field=${field}&method=${method}&order=${currentSortOrder}`);
                const json = await res.json();

                if (res.ok) {
                    currentPage = 1;
                    dataMahasiswa = json.data;
                    renderTable();

                    let hint = "O(n^2)";
                    if (method === "merge" || method === "shell") hint = "O(n log n)";
                    updateExecInfo("/api/mahasiswa/sort", json.execution_time_ms, method.toUpperCase() + ` (${currentSortOrder.toUpperCase()})`, hint);

                    // Update table header icons
                    document.querySelectorAll('.sortable i').forEach(i => i.className = 'bi bi-arrow-down-up ms-1 text-muted');
                    el.querySelector('i').className = currentSortOrder === 'asc' ? 'bi bi-arrow-down ms-1 text-primary fw-bold' : 'bi bi-arrow-up ms-1 text-primary fw-bold';
                } else {
                    showToast("Error Urut Data", json.detail, "danger");
                }
            } catch (err) {
                showToast("Gagal Urut", err.message, "danger");
            }
        });
    });
});
