// ==========================================
// History Elements
// ==========================================

const historyTable = document.getElementById("historyTable");
const searchInput = document.getElementById("searchInput");
const typeFilter = document.getElementById("typeFilter");
const resultFilter = document.getElementById("resultFilter");

let allHistory = [];

// ==========================================
// Load History
// ==========================================

async function loadHistory() {

    if (!currentUser) {

        alert("User not found.");

        return;

    }

    try {

        const response = await fetch(`/api/history/${currentUser.id}`);

        const data = await response.json();

        console.log(data);

        historyTable.innerHTML = "";

        if (!data.success) {

            historyTable.innerHTML = `
                <tr>
                    <td colspan="6">Unable to load history.</td>
                </tr>
            `;

            return;

        }

        allHistory = data.history;

        renderTable(allHistory);

    }

    catch (error) {

        console.error(error);

    }

}

// ==========================================
// Render Table
// ==========================================

function renderTable(history) {

    historyTable.innerHTML = "";

    if (history.length === 0) {

        historyTable.innerHTML = `
            <tr>
                <td colspan="6">No scan history found.</td>
            </tr>
        `;

        return;

    }

    history.forEach(scan => {

        const color =
            scan.prediction === "Real"
            ? "#22c55e"
            : "#ef4444";

        const badge =
            scan.prediction === "Real"
            ? "✅ Real"
            : "⚠ Deepfake";

        historyTable.innerHTML += `
            <tr>

                <td>${scan.filename}</td>

                <td>${scan.type}</td>

                <td style="color:${color};font-weight:600;">
                    ${badge}
                </td>

                <td>${scan.confidence}%</td>

                <td>${scan.date}</td>

                <td>
                    <button
                        class="table-btn"
                        onclick="deleteScan(${scan.id})">
                        Delete
                    </button>
                </td>

            </tr>
        `;

    });

}

// ==========================================
// Filters
// ==========================================

function applyFilters() {

    const search = searchInput.value.toLowerCase();

    const type = typeFilter.value;

    const result = resultFilter.value;

    const filtered = allHistory.filter(scan => {

        const matchSearch =
            scan.filename.toLowerCase().includes(search);

        const matchType =
            type === "All" || scan.type === type;

        const matchResult =
            result === "All" || scan.prediction === result;

        return matchSearch && matchType && matchResult;

    });

    renderTable(filtered);

}

// ==========================================
// Delete Scan
// ==========================================

async function deleteScan(id) {

    if (!confirm("Delete this scan?")) {

        return;

    }

    try {

        const response = await fetch(`/api/history/${id}`, {

            method: "DELETE"

        });

        const result = await response.json();

        alert(result.message);

        loadHistory();

    }

    catch (error) {

        console.error(error);

    }

}

// ==========================================
// Events
// ==========================================

searchInput.addEventListener("input", applyFilters);

typeFilter.addEventListener("change", applyFilters);

resultFilter.addEventListener("change", applyFilters);

// ==========================================
// Initial Load
// ==========================================

loadHistory();