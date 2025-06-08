async function onDownload() {
    // Get the image element
    const image = document.getElementById('img01');
    // alert(image.alt);

    // Fetch the image as a blob
    const response = await fetch(image.src);
    const blob = await response.blob();

    try {
        // Open the "Save As" dialog using the File System Access API
        const fileHandle = await window.showSaveFilePicker({
            // suggestedName: 'image_name.png', // Default file name
            suggestedName: image.alt,
            types: [{
                description: 'Image Files',
                accept: { 'image/jpeg': ['.jpg', '.jpeg'], 'image/png': ['.png'] },
            }],
        });

        // Create a writable stream to the selected file
        const writableStream = await fileHandle.createWritable();

        // Write the image blob to the file
        await writableStream.write(blob);

        // Close the stream
        await writableStream.close();

        alert('Image saved successfully!');
    } catch (error) {
        // Handle errors (e.g., user canceled the dialog)
        if (error.name === 'AbortError') {
            alert('File save canceled.');
        } else {
            console.error('Error saving file:', error);
            alert('Failed to save image.');
        }
    }
}

// Attach the onDownload function to the button's click event
// document.getElementById('saveButton').addEventListener('click', onDownload);

function validateZeroDecimalInput(e) {
    const key = e.key;
    const value = e.target.value;
    const cursorPos = e.target.selectionStart;

    // Allow control keys
    if (['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab'].includes(key)) {
        return true;
    }

    // First character must be '0'
    if (value.length === 0 && key !== '0') {
        return false;
    }

    // Second character must be '.'
    if (value.length === 1 && key !== '.') {
        return false;
    }

    // After decimal, allow only digits (0-9)
    if (value.length >= 2) {
        // Don't allow more than 4 decimal digits
        if (value.split('.')[1]?.length >= 4) {
            return false;
        }
        return /[0-9]/.test(key);
    }

    return true;
}

function validateZeroDecimalFormat(input) {
    const errorElement = document.getElementById('alpha1-error');
    const value = input.value;

    // Allow partial input while typing
    const partialPattern = /^(0|0\.|0\.\d{0,4})$/;

    if (!partialPattern.test(value)) {
        // Auto-correct to last valid state
        const match = value.match(/^(0|0\.|0\.\d{0,4})/);
        input.value = match ? match[0] : '';
    }

    errorElement.style.display = 'none';
}

function validateZeroDecimalFinal(input) {
    const errorElement = document.getElementById('alpha1-error');
    const value = input.value;

    // Final validation: must be exactly 0.xxxx
    if (value && !/^0\.\d{4}$/.test(value)) {
        errorElement.style.display = 'block';
        input.value = '';
        input.focus();
    } else {
        errorElement.style.display = 'none';
    }
}

function showLoader() {
    const loader = document.getElementById('loader');
    loader.classList.add('active');
}

function hideLoader() {
    const loader = document.getElementById('loader');
    loader.classList.remove('active');
}

function handleFormSubmit(event) {
    // Check if all fields are valid
    const form = event.target;

    if (form.checkValidity()) {
        showLoader();  // call only if valid
        return true;   // allow form to submit
    } else {
        event.preventDefault(); // stop form submission
        form.reportValidity();  // show built-in validation messages
        return false;
    }
}

async function fetchData() {
    const responseDiv = document.getElementById('response');
    responseDiv.classList.remove('show');
    responseDiv.textContent = '';
    showLoader();
    try {
        // Simulate an API call with a 2-second delay
        const response = await new Promise(resolve => {
            setTimeout(() => {
                resolve({ data: 'Data retrieved successfully!' });
            }, 2000);
        });
        responseDiv.textContent = response.data;
        responseDiv.classList.add('show');
    } catch (error) {
        responseDiv.textContent = 'Error retrieving data';
        responseDiv.classList.add('show');
    } finally {
        hideLoader();
    }
}