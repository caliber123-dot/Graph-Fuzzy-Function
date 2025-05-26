
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
            
            if(data.cut_id == "1")
            {
                document.getElementById("tr1").style.display = "block";
                document.getElementById("tr2").style.display = "block";
                document.getElementById("tr3").style.display = "block";
                document.getElementById("tr4").style.display = "none";
                document.getElementById("tr5").style.display = "none";
                document.getElementById("tr6").style.display = "none";
            }                
            else if(data.cut_id == "2")
            {
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

// Add event listener to run the fetch when material is selected
document.getElementById("ddlalphacut").addEventListener("change", fetchAlphaData);
document.getElementById("ddlmaterials").addEventListener("change", fetchAlphaData);
document.getElementById("ddlfuntion").addEventListener("change", fetchAlphaData); // optional if you want dynamic update when fm_id is changed

