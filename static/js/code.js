
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

//For Index Page
function ExportToExcel() {
    const imageIds = ['gr1', 'gr2', 'gr3', 'gr4'];
    const arrexp = [];
    const fnDict = document.getElementById('fn_dict').value;
    const fnDictDash = document.getElementById('fn_dict_dash').value;
    const Tfn = document.getElementById('ddlfuntion');
    const Material = document.getElementById('ddlmaterials');
    let filename = '';
    if (Tfn.selectedIndex == 0) {
        alert('Select Fuzzy Membership Function');
        return;
    }
    if (Material.selectedIndex == 0) {
        alert('Select Materials');
        return;
    }
    else if (Tfn.selectedIndex == 1) {
        const selectedMaterial = Material.options[Material.selectedIndex].text.trim();
        // alert(selectedMaterial);               
        if (selectedMaterial == 'Aluminium')
            filename = "Trapezoidal_" + "AL"
        else if (selectedMaterial == 'Neoprene Rubber')
            filename = "Trapezoidal_" + "NR"
        else if (selectedMaterial == 'Teflon')
            filename = "Trapezoidal_" + "TF"
        else if (selectedMaterial == 'Nylon')
            filename = "Trapezoidal_" + "NL"
        else if (selectedMaterial == 'SS-304 Grade ABS Silicon')
            filename = "Trapezoidal_" + "SS304"
    }
    else if (Tfn.selectedIndex == 2) {
        const selectedMaterial = Material.options[Material.selectedIndex].text.trim();
        if (selectedMaterial == 'Aluminium')
            filename = "Triangular_" + "AL"
        else if (selectedMaterial == 'Neoprene Rubber')
            filename = "Triangular_" + "NR"
        else if (selectedMaterial == 'Teflon')
            filename = "Triangular_" + "TF"
        else if (selectedMaterial == 'Nylon')
            filename = "Triangular_" + "NL"
        else if (selectedMaterial == 'SS-304 Grade ABS Silicon')
            filename = "Triangular_" + "SS304"
    }
    // Collect image filenames
    for (const id of imageIds) {
        const img = document.getElementById(id);
        if (img && !img.src.toLowerCase().endsWith('.avif')) {
            arrexp.push(img.alt);
        }
    }
    const formData = new FormData();
    // formData.append('alpha_cuts', alphaCuts);
    formData.append('fn_dict', fnDict);
    formData.append('fn_dict_dash', fnDictDash);
    formData.append('file1', arrexp[0]);
    formData.append('file2', arrexp[1]);
    formData.append('file3', arrexp[2]);
    formData.append('file4', arrexp[3]);
    // alert(fnDictDash)
    if (filename == '')
        filename = 'exported_charts';
    
    let filetitle = '';
    const sm = Material.options[Material.selectedIndex].text.trim();
    if (Tfn.selectedIndex == 1)    
        filetitle = "Trapezoidal Fuzzy Function for " + sm;
    else if (Tfn.selectedIndex == 2)
        filetitle = "Triangular Fuzzy Function for " + sm;

    // alert(filetitle);
    formData.append('filetitle', filetitle);
    // filename
    // alert(filename);
    // Show loading state
    const exportBtn = document.querySelector('[onclick="ExportToExcel()"]');
    exportBtn.disabled = true;
    exportBtn.textContent = 'Exporting...';

    // fetch(`/export_excel/${encodeURIComponent(arrexp[0])}/${encodeURIComponent(arrexp[1])}`)
    fetch('/export_excel2', {
        method: 'POST',
        body: formData // Automatically sets 'multipart/form-data'
    })
        .then(async response => {
            if (!response.ok) {
                const error = await response.json().catch(() => ({ error: response.statusText }));
                throw new Error(error.message || 'Export failed');
            }
            return response.blob();
        })
        .then(blob => {
            // Create download link
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename + '_LineChart' + '.xlsx';
            document.body.appendChild(a);
            a.click();

            // Show success message
            alert('Excel file exported successfully!');

            // Clean up
            setTimeout(() => {
                URL.revokeObjectURL(url);
                document.body.removeChild(a);
            }, 100);
        })
        .catch(error => {
            console.error('Export error:', error);
            alert(`Export failed: ${error.message}`);
        })
        .finally(() => {
            exportBtn.disabled = false;
            exportBtn.textContent = 'Export to Excel';
        });
}

