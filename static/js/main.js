async function processCipher(action) {
    try {
        const text = document.getElementById('inputText').value;
        const key = document.getElementById('key').value;
        const key2 = document.getElementById('key2').value;
        const cipherType = document.getElementById('cipherType').value;
        
        // Log the input values
        console.log('Input values:', { text, key, key2, cipherType, action });

        const response = await fetch(`/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                key: key,
                key2: key2,
                cipher_type: cipherType
            })
        });
        
        // Log the raw response
        console.log('Raw response:', response);
        
        const data = await response.json();
        console.log('Response data:', data);  // Log the response data
        
        if (data.success) {
            document.getElementById('result').value = data.result;
            
            // Handle visualization
            const gridContainer = document.getElementById('gridContainer');
            if (cipherType === 'double-columnar' && data.visualization) {
                gridContainer.style.display = 'block';
                gridContainer.innerHTML = `
                    <div class="grid-title">Double Columnar Grids:</div>
                    <pre>${data.visualization.first_grid_str}</pre>
                    <pre>${data.visualization.second_grid_str}</pre>
                `;
            }
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Detailed error:', error);  // Log the detailed error
        alert('Error processing request. Check console for details.');
    }
}

// Add event listener for cipher type changes
document.getElementById('cipherType').addEventListener('change', function(e) {
    const key2Input = document.getElementById('key2');
    if (e.target.value === 'double-columnar') {
        key2Input.style.display = 'block';
    } else {
        key2Input.style.display = 'none';
        key2Input.value = ''; // Clear the second key when not needed
    }
});