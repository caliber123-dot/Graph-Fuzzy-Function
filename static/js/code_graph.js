
function fetchAlphaData() {
    const matId = document.getElementById("ddlmaterials").value;
    const fm_id = document.getElementById("ddlfuntion").value;
    const cut_id = document.getElementById("ddlalphacut").value;
    // alert("Hello!!!");
    // Check both values are selected
    // if (!matId || !fm_id || matId === "Other") {
    //     clearAlphaFields();
    //     return;
    // }

    fetch(`/get_alpha_data_cut/${matId}/${fm_id}//${cut_id}`)
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

            document.getElementById("alphadash11").value = data.alpha1 || "";
            document.getElementById("alphadash22").value = data.alpha2 || "";
            document.getElementById("alphadash33").value = data.alpha3 || "";

            if (data.cut_id == "1") {
                document.getElementById("tr1").style.display = "block";
                document.getElementById("tr2").style.display = "block";
                document.getElementById("tr3").style.display = "block";
                document.getElementById("tr4").style.display = "none";
                document.getElementById("tr5").style.display = "none";
                document.getElementById("tr6").style.display = "none";
            }
            else if (data.cut_id == "2") {
                document.getElementById("tr1").style.display = "none";
                document.getElementById("tr2").style.display = "none";
                document.getElementById("tr3").style.display = "none";
                document.getElementById("tr4").style.display = "block";
                document.getElementById("tr5").style.display = "block";
                document.getElementById("tr6").style.display = "block";
            }
            // document.getElementById("cut_id").value = data.cut_id || "";
            // document.getElementById("alphaButton").textContent = "Update Alpha Graph";
            // document.getElementById("alphaButton").style.backgroundColor = "#007bff";  // Blue
        })
        .catch(error => {
            // clearAlphaFields();
            console.log("No alpha data found.");
            // document.getElementById("alphaButton").textContent = "Create Alpha Graph";
            // document.getElementById("alphaButton").style.backgroundColor = "#28a745";  // Green
        });
}

function clearAlphaFields() {
    ["alpha1", "alpha2", "alpha3", "alphadash1", "alphadash2", "alphadash3"].forEach(id => {
        document.getElementById(id).value = "";
    });
}

function ExportToExcel() {
    const imageIds = ['gr1', 'gr2', 'gr3', 'gr4'];
    const arrexp = [];
    const fnDict = document.getElementById('fn_dict').value;
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
            filename = "Natural_Frequency_Trapezoidal_" + "AL"
        else if (selectedMaterial == 'Neoprene Rubber')
            filename = "Natural_Frequency_Trapezoidal_" + "NR"
        else if (selectedMaterial == 'Teflon')
            filename = "Natural_Frequency_Trapezoidal_" + "TF"
        else if (selectedMaterial == 'Nylon')
            filename = "Natural_Frequency_Trapezoidal_" + "NL"
        else if (selectedMaterial == 'SS-304 Grade ABS Silicon')
            filename = "Natural_Frequency_Trapezoidal_" + "SS304"
    }
    else if (Tfn.selectedIndex == 2) {
        const selectedMaterial = Material.options[Material.selectedIndex].text.trim();
        if (selectedMaterial == 'Aluminium')
            filename = "Natural_Frequency_Triangular_" + "AL"
        else if (selectedMaterial == 'Neoprene Rubber')
            filename = "Natural_Frequency_Triangular_" + "NR"
        else if (selectedMaterial == 'Teflon')
            filename = "Natural_Frequency_Triangular_" + "TF"
        else if (selectedMaterial == 'Nylon')
            filename = "Natural_Frequency_Triangular_" + "NL"
        else if (selectedMaterial == 'SS-304 Grade ABS Silicon')
            filename = "Natural_Frequency_Triangular_" + "SS304"
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
    formData.append('file1', arrexp[1]);
    // alert(arrexp[1])
    if (filename == '')
        filename = 'exported_charts';

    let filetitle = '';
    const sm = Material.options[Material.selectedIndex].text.trim();
    if (Tfn.selectedIndex == 1)
        filetitle = "Trapezoidal Fuzzy Function for " + sm;
    else if (Tfn.selectedIndex == 2)
        filetitle = "Triangular Fuzzy Function for " + sm;

    formData.append('filetitle', filetitle);

    // Show loading state
    const exportBtn = document.querySelector('[onclick="ExportToExcel()"]');
    exportBtn.disabled = true;
    exportBtn.textContent = 'Exporting...';

    // fetch(`/export_excel/${encodeURIComponent(arrexp[0])}/${encodeURIComponent(arrexp[1])}`)
    fetch('/export_excel', {
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
            a.download = filename + '_BarChart' + '.xlsx';
            // a.download = 'exported_charts.xlsx';
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

// Add event listener to run the fetch when material is selected
document.getElementById("ddlalphacut").addEventListener("change", fetchAlphaData);
document.getElementById("ddlmaterials").addEventListener("change", fetchAlphaData);
document.getElementById("ddlfuntion").addEventListener("change", fetchAlphaData); // optional if you want dynamic update when fm_id is changed

