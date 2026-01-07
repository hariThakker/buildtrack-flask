let totalExpense = 0;

// DELETE PROJECT (GLOBAL)
function deleteProject(id) {
    if (!confirm("Are you sure you want to delete this project?")) return;

    fetch(`/projects/${id}`, {
        method: "DELETE"
    })
        .then(res => {
            if (!res.ok) throw new Error("Delete failed");
            alert("Project deleted successfully");
            location.reload();
        })
        .catch(err => {
            alert("Error deleting project");
            console.error(err);
        });
}

// LOAD DASHBOARD DATA
fetch("/projects")
    .then(res => res.json())
    .then(projects => {
        document.getElementById("totalProjects").innerText = projects.length;

        const table = document.getElementById("projectTable");
        table.innerHTML = "";
        totalExpense = 0;

        projects.forEach((p, index) => {

            // Fetch summary for expense calculation
            fetch(`/projects/${p.id}/summary`)
                .then(res => res.json())
                .then(summary => {
                    totalExpense += summary.total_expense;
                    document.getElementById("totalExpense").innerText = "₹" + totalExpense;
                });

            // Render table row
            table.innerHTML += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${p.name}</td>
                    <td>${p.client}</td>
                    <td>${p.location}</td>
                    <td>
                        <a class="btn btn-sm btn-primary"
                           href="/ui/summary/${p.id}">
                           View
                        </a>
                        <button class="btn btn-sm btn-danger"
                                onclick="deleteProject(${p.id})">
                           Delete
                        </button>
                    </td>
                </tr>
            `;
        });
    });
