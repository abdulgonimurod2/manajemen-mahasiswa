const API_URL = "/api/mahasiswa";

let dataMahasiswa = [];
let currentPage = 1;
const MAX_PER_PAGE = 10;

document.addEventListener("DOMContentLoaded", () => {
    if (window.location.pathname.includes("dashboard.html")) {
        loadData();

        document.getElementById("btnSave").addEventListener("click", saveMahasiswa);
        document.getElementById("btnExport").addEventListener("click", exportData);

        document.getElementById("btnAdd").addEventListener("click", () => {
            document.getElementById("formMode").value = "add";
            document.getElementById("formMahasiswa").reset();
            document.getElementById("formNim").readOnly = false;
            document.getElementById("modalTitle").textContent = "Tambah Mahasiswa";
            const modal = new bootstrap.Modal(document.getElementById("formModal"));
            modal.show();
        });
    }
});

window.exportData = function () {
    window.location.href = `${API_URL}/export/csv`;
}

window.handleImport = async function (event) {
    const file = event.target.files[0];
    if (!file) return;

    // Custom button process indication
    const btnImport = document.getElementById("btnImport");
    const originalContent = btnImport.innerHTML;
    btnImport.innerHTML = `<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>`;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch(`${API_URL}/import/csv`, {
            method: "POST",
            body: formData
        });
        const json = await res.json();

        if (res.ok) {
            showToast("Berhasil Import", json.message, "success");
            loadData();
        } else {
            showToast("Gagal Import", json.message || json.detail, "danger");
        }
    } catch (err) {
        showToast("Error Import", err.message, "danger");
    } finally {
        btnImport.innerHTML = originalContent;
        event.target.value = ""; // reset file input
    }
}

async function loadData() {
    try {
        const res = await fetch(API_URL);
        const json = await res.json();
        if (res.ok) {
            dataMahasiswa = json.data;
            updateExecInfo("GET /api/mahasiswa", json.execution_time_ms, "Read File", "O(n)");
            renderTable();
            updateStats();
        } else {
            showToast("Error", json.detail || "Gagal memuat data", "danger");
        }
    } catch (err) {
        showToast("Error", err.message, "danger");
    }
}

window.updateExecInfo = function (endpoint, time_ms, method, hint) {
    const box = document.getElementById("execInfo");
    if (!box) return;
    box.innerHTML = `${endpoint} - Algoritma: <b>${method}</b> - Waktu: <b>${time_ms.toFixed(3)} ms</b> <br> Hint: ${hint}`;
}

function getStatusBadge(status) {
    const map = {
        "Aktif": "bg-success-subtle text-success",
        "Cuti": "bg-warning-subtle text-warning",
        "Lulus": "bg-info-subtle text-info",
        "DO": "bg-danger-subtle text-danger border"
    };
    return `<span class="badge ${map[status] || "bg-secondary"} badge-status shadow-sm border border-light">${status}</span>`;
}

window.renderTable = function (data = dataMahasiswa) {
    const tb = document.getElementById("tableBody");
    tb.innerHTML = "";

    const start = (currentPage - 1) * MAX_PER_PAGE;
    const end = start + MAX_PER_PAGE;
    const paginatedItems = data.slice(start, end);

    paginatedItems.forEach((m, idx) => {
        tb.innerHTML += `
            <tr>
                <td class="ps-4 text-muted">${start + idx + 1}</td>
                <td class="fw-medium text-dark">${m.nim}</td>
                <td class="fw-bold text-dark">${m.nama}</td>
                <td class="fw-bold text-dark">${m.email}</td>
                <td class="text-secondary">${m.jurusan}</td>
                <td class="text-secondary">${m.angkatan}</td>
                <td class="font-monospace fw-medium">${typeof m.ipk === 'number' ? m.ipk.toFixed(2) : parseFloat(m.ipk).toFixed(2)}</td>
                <td>${getStatusBadge(m.status)}</td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-light border text-primary shadow-sm me-1" onclick="editData('${m.nim}')"><i class="bi bi-pencil-square"></i></button>
                    <button class="btn btn-sm btn-light border text-danger shadow-sm" onclick="deleteData('${m.nim}')"><i class="bi bi-trash"></i></button>
                </td>
            </tr>
        `;
    });

    renderPagination(data.length);
}

function renderPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / MAX_PER_PAGE);
    const ul = document.getElementById("pagination");
    const info = document.getElementById("paginationInfo");

    if (totalItems === 0) {
        info.innerHTML = "Menampilkan <span class='fw-bold'>0</span> data";
        ul.innerHTML = "";
        return;
    }

    const start = (currentPage - 1) * MAX_PER_PAGE + 1;
    const end = Math.min(currentPage * MAX_PER_PAGE, totalItems);
    info.innerHTML = `Menampilkan <span class="fw-bold">${start}-${end}</span> dari <span class="fw-bold">${totalItems}</span> data`;

    ul.innerHTML = "";
    for (let i = 1; i <= totalPages; i++) {
        ul.innerHTML += `<li class="page-item ${i === currentPage ? 'active' : ''}"><a class="page-link shadow-sm border-0 ${i === currentPage ? 'bg-primary text-white' : 'text-dark'}" href="#" onclick="changePage(${i}); return false;">${i}</a></li>`;
    }
}

window.changePage = function (page) {
    currentPage = page;
    renderTable();
}

function updateStats() {
    document.getElementById("statTotal").textContent = dataMahasiswa.length;
    document.getElementById("statAktif").textContent = dataMahasiswa.filter(m => m.status === 'Aktif').length;
    document.getElementById("statCuti").textContent = dataMahasiswa.filter(m => m.status === 'Cuti').length;
    document.getElementById("statLulus").textContent = dataMahasiswa.filter(m => m.status === 'Lulus').length;
}

async function saveMahasiswa() {
    const form = document.getElementById("formMahasiswa");
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    // Custom button process indication
    const btnSave = document.getElementById("btnSave");
    const originalText = btnSave.innerHTML;
    btnSave.innerHTML = `<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span> Loading...`;

    const mode = document.getElementById("formMode").value;
    const nim = document.getElementById("formNim").value;

    const payload = {
        nim: nim,
        nama: document.getElementById("formNama").value,
        jurusan: document.getElementById("formJurusan").value,
        angkatan: parseInt(document.getElementById("formAngkatan").value),
        ipk: parseFloat(document.getElementById("formIpk").value),
        status: document.getElementById("formStatus").value,
        no_telp: document.getElementById("formTelp").value,
        email: document.getElementById("formEmail").value
    };

    const url = mode === "add" ? API_URL : `${API_URL}/${document.getElementById("oldNim").value}`;
    const method = mode === "add" ? "POST" : "PUT";

    try {
        const res = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const json = await res.json();

        btnSave.innerHTML = originalText;

        if (res.ok) {
            bootstrap.Modal.getInstance(document.getElementById("formModal")).hide();
            showToast("Berhasil", json.message, "success");
            loadData();
        } else {
            showToast("Perhatian Ditolak", json.detail, "danger");
        }
    } catch (err) {
        btnSave.innerHTML = originalText;
        showToast("Error System", err.message, "danger");
    }
}

window.editData = function (nim) {
    const m = dataMahasiswa.find(x => x.nim === nim);
    if (!m) return;

    document.getElementById("formMode").value = "edit";
    document.getElementById("oldNim").value = m.nim;
    document.getElementById("formNim").value = m.nim;
    document.getElementById("formNim").readOnly = true;

    document.getElementById("formNama").value = m.nama;
    document.getElementById("formJurusan").value = m.jurusan;
    document.getElementById("formAngkatan").value = m.angkatan;
    document.getElementById("formIpk").value = m.ipk;
    document.getElementById("formStatus").value = m.status;
    document.getElementById("formTelp").value = m.no_telp;
    document.getElementById("formEmail").value = m.email;

    document.getElementById("modalTitle").textContent = "Edit Data Mahasiswa";
    const modal = new bootstrap.Modal(document.getElementById("formModal"));
    modal.show();
}

window.deleteData = async function (nim) {
    if (!confirm("Peringatan: Yakin ingin menghapus data dengan NIM " + nim + "?")) return;

    try {
        const res = await fetch(`${API_URL}/${nim}`, { method: "DELETE" });
        const json = await res.json();
        if (res.ok) {
            showToast("Dihapus", json.message, "success");
            loadData();
        } else {
            showToast("Error Hapus", json.detail, "danger");
        }
    } catch (err) {
        showToast("Fatal Error", err.message, "danger");
    }
}

window.showToast = function (title, message, type) {
    const container = document.getElementById("toastContainer");
    const id = "toast_" + Date.now();
    const bg = type === "success" ? "bg-success text-white" : "bg-danger text-white";
    const icon = type === "success" ? "bi-check-circle" : "bi-exclamation-triangle";

    const html = `
        <div id="${id}" class="toast align-items-center border-0 mb-3 shadow-lg" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header ${bg}">
                <i class="bi ${icon} me-2"></i>
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>    
            <div class="toast-body bg-white text-dark">
                ${message}
            </div>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', html);
    const toast = new bootstrap.Toast(document.getElementById(id));
    toast.show();
    setTimeout(() => { document.getElementById(id)?.remove(); }, 5000);
}
