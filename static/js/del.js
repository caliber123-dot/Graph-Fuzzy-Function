document.getElementById("ddlfuntion").addEventListener("change", function () {
    const functionId = this.value;
    // clearAlphaFields();

    const tableBody = document.getElementById("materialsTableBody");
    tableBody.innerHTML = ''; // Clear previous materials

    if (functionId) {
        fetch(`/get_materials/${functionId}`)
            .then(response => {
                if (!response.ok) throw new Error("Failed to load materials");
                return response.json();
            })
            .then(materials => {
                if (materials.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="2">No materials found.</td></tr>';
                    return;
                }

                materials.forEach(mat => {
                    const row = document.createElement("tr");
                    row.id = `row_${mat.mat_id}`;
                    row.innerHTML = `
                        <td>${mat.mat_name}</td>
                        <td class="action-cell">
                            <button type="button" style="color:red" onclick="return submitMaterial('${mat.mat_id}', '${mat.mat_name}')" ><i class="fa fa-trash" aria-hidden="true"></i> </button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error("Error fetching materials:", error);
                tableBody.innerHTML = '<tr><td colspan="2">Error loading materials.</td></tr>';
            });
    }
});

function submitMaterial(id, mat) {
    const confirmed = confirm(`Are you sure you want to delete "${mat}"?`);
    if (confirmed) {
        fetch('/del_mat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mat_id: id })
        })
        .then(response => {
            if (!response.ok) throw new Error("Delete failed.");
            return response.json();
        })
        .then(data => {
            alert(data.message);
            // Remove row from UI
            const row = document.getElementById(`row_${id}`);
            if (row) row.remove();
        })
        .catch(error => {
            console.error("Delete error:", error);
            alert("Error deleting material.");
        });
    }
}

function submitMaterial000(id, mat) {
    // alert(id + mat);
    const confirmed = confirm(`Are you sure you want to delete "${mat}"?`);
    if (confirmed) {
        // Call Flask route using fetch or form submission
        fetch(`/del_mat/${id}`, {
            method: 'DELETE'  // or 'POST' depending on your Flask route
        })
        .then(response => {
            if (!response.ok) throw new Error("Delete failed.");
            alert(`Material "${mat}" deleted successfully.`);
            // Optionally remove row from DOM
            const row = document.getElementById(`row_${id}`);
            if (row) row.remove();
        })
        .catch(error => {
            console.error("Delete error:", error);
            alert("Something went wrong while deleting.");
        });
        return true;
    }
    else
        return false;
}
