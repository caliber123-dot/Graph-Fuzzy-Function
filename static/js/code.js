
function fetchAlphaData() {
    const matId = document.getElementById("ddlmaterials").value;
    const fm_id = document.getElementById("ddlfuntion").value;

    // Check both values are selected
    if (!matId || !fm_id || matId === "Other") {
        clearAlphaFields();
        return;
    }

    fetch(`/get_alpha_data/${matId}/${fm_id}`)
        .then(response => {
            if (!response.ok) throw new Error("No data found");
            return response.json();
        })
        .then(data => {
            document.getElementById("alpha1").value = data.alpha1 || "";
            document.getElementById("alpha2").value = data.alpha2 || "";
            document.getElementById("alpha3").value = data.alpha3 || "";
            document.getElementById("alphadash1").value = data.alphadash1 || "";
            document.getElementById("alphadash2").value = data.alphadash2 || "";
            document.getElementById("alphadash3").value = data.alphadash3 || "";
            document.getElementById("alpha_id").value = data.alpha_id || "";
            // document.getElementById("alphaButton").textContent = "Update Alpha Graph";
            document.getElementById("alphaButton").style.backgroundColor = "#007bff";  // Blue
        })
        .catch(error => {
            clearAlphaFields();
            console.log("No alpha data found.");
            document.getElementById("alphaButton").textContent = "Create Alpha Graph";
            document.getElementById("alphaButton").style.backgroundColor = "#28a745";  // Green
        });
}

function clearAlphaFields() {
    ["alpha1", "alpha2", "alpha3", "alphadash1", "alphadash2", "alphadash3", "alpha_id"].forEach(id => {
        document.getElementById(id).value = "";
    });
}


// Add event listener to run the fetch when material is selected
document.getElementById("ddlmaterials").addEventListener("change", fetchAlphaData);
// document.getElementById("ddlfuntion").addEventListener("change", fetchAlphaData); // optional if you want dynamic update when fm_id is changed

document.getElementById("ddlfuntion").addEventListener("change", function () {
    const functionId = this.value;
    clearAlphaFields();
    if (functionId) {
        fetch(`/get_materials/${functionId}`)
            .then(response => {
                if (!response.ok) throw new Error("Failed to load materials");
                return response.json();
            })
            .then(materials => {
                const ddlMaterials = document.getElementById("ddlmaterials");
                ddlMaterials.innerHTML = '<option value="">Select Materials.</option>';
                materials.forEach(mat => {
                    const option = document.createElement("option");
                    option.value = mat.mat_id;
                    option.textContent = mat.mat_name;
                    ddlMaterials.appendChild(option);
                });
            })
            .catch(error => {
                console.error("Error fetching materials:", error);
            });
    }
});



   