
function fetchAlphaData() {
    const matId = document.getElementById("ddlmaterials").value;
    const fm_id = document.getElementById("ddlfuntion").value;
    const Material = document.getElementById('ddlmaterials');
    const selectedMaterial = Material.options[Material.selectedIndex].text.trim();
    document.getElementById("txtmaterial").value = selectedMaterial;

    fetch(`/get_material_data/${matId}/${fm_id}`)
        .then(response => {
            if (!response.ok) throw new Error("No data found");
            return response.json();
        })
        .then(data => {
            document.getElementById("a_value_d").value = data.a_val_d || "";
            document.getElementById("b_value_d").value = data.b_val_d || "";
            document.getElementById("c_value_d").value = data.c_val_d || "";
            document.getElementById("d_value_d").value = data.d_val_d || "";

            document.getElementById("a_value_y").value = data.a_val_y || "";
            document.getElementById("b_value_y").value = data.b_val_y || "";
            document.getElementById("c_value_y").value = data.c_val_y || "";
            document.getElementById("d_value_y").value = data.d_val_y || "";
            
        })
        .catch(error => {
            clearAlphaFields();
            console.log("No alpha data found.");
            // document.getElementById("alphaButton").textContent = "Create Alpha Graph";
            // document.getElementById("alphaButton").style.backgroundColor = "#28a745";  // Green
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

function clearAlphaFields() {
    ["a_value_d", "a_value_y", "b_value_d", "b_value_y", "c_value_d", "c_value_y","d_value_d","d_value_y"].forEach(id => {
        document.getElementById(id).value = "";
    });
}
