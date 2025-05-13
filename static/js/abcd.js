
function fetchAlphaData() {
    const matId = document.getElementById("ddlmaterials").value;
    const fm_id = document.getElementById("ddlfuntion").value;

    fetch(`/get_material_data/${matId}/${fm_id}`)
        .then(response => {
            if (!response.ok) throw new Error("No data found");
            return response.json();
        })
        .then(data => {
            document.getElementById("a_value").value = data.alpha1 || "";
            document.getElementById("b_value").value = data.alpha2 || "";
            document.getElementById("c_value").value = data.alpha3 || "";
            document.getElementById("d_value").value = data.alphadash1 || "";
            // document.getElementById("alphadash2").value = data.alphadash2 || "";
            // document.getElementById("alphadash3").value = data.alphadash3 || "";
            // document.getElementById("alpha_id").value = data.alpha_id || "";
            // document.getElementById("alphaButton").textContent = "Update Alpha Graph";
            // document.getElementById("alphaButton").style.backgroundColor = "#007bff";  // Blue
        })
        .catch(error => {
            clearAlphaFields();
            console.log("No alpha data found.");
            document.getElementById("alphaButton").textContent = "Create Alpha Graph";
            document.getElementById("alphaButton").style.backgroundColor = "#28a745";  // Green
        });
}

// Add event listener to run the fetch when material is selected
document.getElementById("ddlmaterials").addEventListener("change", fetchAlphaData);
// document.getElementById("ddlfuntion").addEventListener("change", fetchAlphaData); // optional if you want dynamic update when fm_id is changed

document.getElementById("ddlfuntion").addEventListener("change", function () {
    const functionId = this.value;
    // clearAlphaFields();
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
