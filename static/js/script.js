async function onDownload() {
    // Get the image element
    const image = document.getElementById('img01');

    // Fetch the image as a blob
    const response = await fetch(image.src);
    const blob = await response.blob();

    try {
        // Open the "Save As" dialog using the File System Access API
        const fileHandle = await window.showSaveFilePicker({
            suggestedName: 'image_name.png', // Default file name
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