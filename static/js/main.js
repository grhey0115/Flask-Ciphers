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
            } else if (cipherType === 'aes' && data.visualization) {
                const aesInfoContainer = document.getElementById('aesInfoContainer');
                if (aesInfoContainer) {
                    aesInfoContainer.style.display = 'block';
                    aesInfoContainer.innerHTML = `
                        <div class="viz-title">AES Configuration:</div>
                        <pre>${data.visualization.aes_info}</pre>
                    `;
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

function validateKey(key, cipherType) {
    if (!key) return false;
    
    switch(cipherType) {
        case 'aes':
            // For AES-256, we need exactly 32 characters
            if (key.length !== 32) {
                showError('AES-256 requires exactly 32 characters for the key');
                return false;
            }
            return true;
        // ... other cases remain the same ...
    }
}

// Add this helper function for AES key handling
function processAESCipher(text, key, action) {
    // Ensure the key is exactly 32 characters by padding or truncating
    let processedKey = key;
    if (key.length < 32) {
        processedKey = key.padEnd(32, '0');  // Pad with zeros if too short
    } else if (key.length > 32) {
        processedKey = key.slice(0, 32);     // Truncate if too long
    }

    // Make the AJAX call to the server
    return fetch(`/${action}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            text: text,
            key: processedKey,
            cipher_type: 'aes'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            throw new Error(data.error);
        }
        
        // Handle visualization if available
        if (data.visualization && data.visualization.aes_info) {
            const aesInfoContainer = document.getElementById('aesInfoContainer');
            if (aesInfoContainer) {
                aesInfoContainer.style.display = 'block';
                aesInfoContainer.innerHTML = `<pre>${data.visualization.aes_info}</pre>`;
            }
        }
        
        return data.result;
    });
}

// Update the key input placeholder for AES
document.getElementById('cipherType').addEventListener('change', function(e) {
    const keyInput = document.getElementById('key');
    if (e.target.value === 'aes') {
        keyInput.placeholder = 'Enter 32 character key (will be padded/truncated if needed)';
    }
    // ... rest of the existing change handler ...
});

