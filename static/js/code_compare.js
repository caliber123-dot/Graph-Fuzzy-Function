function ExportToExcel() {
    const imageIds = ['gr1', 'gr2', 'gr3', 'gr4'];
    const arrexp = [];
    const fnDict = document.getElementById('fn_dict').value;
    const Tfn = document.getElementById('ddlfuntion');
    // alert("All.....");
    // const Material = document.getElementById('ddlmaterials');
    let filename = '';
    if (Tfn.selectedIndex == 0) {
        alert('Select Fuzzy Membership Function');
        return;
    }    
    else if (Tfn.selectedIndex == 1) {
        filename = "Comp_Trapezoidal_All_Materials_";        
    }
    else if (Tfn.selectedIndex == 2) {
        filename = "Comp_Triangular_All_Materials_";        
    }
    // Collect image filenames
    for (const id of imageIds) {
        const img = document.getElementById(id);
        if (img && !img.src.toLowerCase().endsWith('.avif')) {
            arrexp.push(img.alt);
        }
    }
    // alert(fnDict);
    const formData = new FormData();
    // formData.append('alpha_cuts', alphaCuts);
    formData.append('fn_dict', fnDict);
    formData.append('file1', arrexp[1]);
    // alert(arrexp[1])
    if (filename == '')
        filename = 'exported_charts';

    let filetitle = '';
    // const sm = Material.options[Material.selectedIndex].text.trim();
    if (Tfn.selectedIndex == 1)
        filetitle = "Trapezoidal Fuzzy Function for all Materials";
    else if (Tfn.selectedIndex == 2)
        filetitle = "Triangular Fuzzy Function for all Materials" ;

    formData.append('filetitle', filetitle);

    // Show loading state
    const exportBtn = document.querySelector('[onclick="ExportToExcel()"]');
    exportBtn.disabled = true;
    exportBtn.textContent = 'Exporting...';

    // fetch(`/export_excel/${encodeURIComponent(arrexp[0])}/${encodeURIComponent(arrexp[1])}`)
    fetch('/export_excel_compare', {
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
