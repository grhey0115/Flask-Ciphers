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
                //gridContainer.style.display = 'block';
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

document.addEventListener('DOMContentLoaded', function() {
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
                    if (gridContainer) {
                        gridContainer.style.display = 'block'; // Ensure the container is shown
                        gridContainer.innerHTML = `
                            <div class="grid-title">Double Columnar Grids:</div>
                            <pre>${data.visualization.first_grid_str}</pre>
                            <pre>${data.visualization.second_grid_str}</pre>
                        `;
                    } else {
                        console.error('Grid container not found.');
                    }
                } else if (cipherType === 'single-columnar' && data.visualization) {
                    if (gridContainer) {
                        gridContainer.style.display = 'block'; // Show the grid container for single-columnar
                        gridContainer.innerHTML = `
                            <div class="grid-title">Single Columnar Grid:</div>
                            <pre>${data.visualization.single_grid_str}</pre>
                        `;
                    } else {
                        console.error('Grid container not found.');
                    }
                } else {
                    // Hide the grid container if no visualization data is available
                    if (gridContainer) {
                        gridContainer.style.display = 'none';
                    }
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
        const gridContainer = document.getElementById('gridContainer');

        if (key2Input) {  // Check if key2Input exists
            if (e.target.value === 'double-columnar') {
                key2Input.style.display = 'block';
            } else {
                key2Input.style.display = 'none';
                key2Input.value = ''; // Clear the second key when not needed
            }
        } else {
            console.error('Key2 input not found.');
        }

        // Hide the grid container for other cipher types
        if (gridContainer) {
            if (e.target.value === 'single-columnar' || e.target.value === 'double-columnar') {
                gridContainer.style.display = 'none'; // Initially hide and show based on the response later
            } else {
                gridContainer.style.display = 'none'; // Hide for other types
            }
        }
    });

    // Add event listeners for encrypt/decrypt buttons
    document.querySelectorAll('.buttons button').forEach(button => {
        button.addEventListener('click', function() {
            const action = this.classList.contains('encrypt') ? 'encrypt' : 'decrypt';
            processCipher(action);
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Hide second key container by default
    const key2Container = document.getElementById('key2Container');
    key2Container.style.display = 'none';

    // Add event listener for cipher type changes
    document.getElementById('cipherType').addEventListener('change', function(e) {
        const key2Container = document.getElementById('key2Container');
        const gridContainer = document.getElementById('gridContainer');
        const singleGridContainer = document.getElementById('singleGridContainer');
        const aesInfoContainer = document.getElementById('aesInfoContainer');
        
        // Hide all visualization containers
        gridContainer.style.display = 'none';
        singleGridContainer.style.display = 'none';
        aesInfoContainer.style.display = 'none';
        
        // Show/hide second key input only for double columnar
        if (e.target.value === 'double-columnar') {
            key2Container.style.display = 'block';
            // Optional: Add animation
            key2Container.style.opacity = '0';
            setTimeout(() => {
                key2Container.style.opacity = '1';
            }, 50);
        } else {
            key2Container.style.display = 'none';
            document.getElementById('key2').value = ''; // Clear second key value
        }
    });
});

