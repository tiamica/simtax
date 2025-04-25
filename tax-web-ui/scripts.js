document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const phoneNumber = document.getElementById('phoneNumber').value;
            window.location.href = `account.html?phone=${encodeURIComponent(phoneNumber)}`;
        });
    }

    const urlParams = new URLSearchParams(window.location.search);
    const phoneNumber = urlParams.get('phone');
    
    if (phoneNumber) {
        fetchAccountData(phoneNumber);
    }
});

function fetchAccountData(phoneNumber) {
    // Fetch basic account information
    fetch(`http://localhost:5000/status/${encodeURIComponent(phoneNumber)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch account data');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }

            // Update the account overview
            document.getElementById('phoneNumber').textContent = phoneNumber;
            document.getElementById('taxCode').textContent = data.tax_code || 'N/A';
            document.getElementById('status').textContent = data.status || 'No status available';

            // Fetch yearly returns
            const years = [2023, 2022, 2021];
            const returnsContainer = document.getElementById('yearlyReturns');
            returnsContainer.innerHTML = '';

            years.forEach(year => {
                fetch(`http://localhost:5000/status/${encodeURIComponent(phoneNumber)}/${year}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`Failed to fetch ${year} return`);
                        }
                        return response.json();
                    })
                    .then(returnData => {
                        if (returnData.error) {
                            throw new Error(returnData.error);
                        }

                        const returnDiv = document.createElement('div');
                        returnDiv.className = 'return-item';
                        returnDiv.innerHTML = `
                            <h4>${year} Tax Return</h4>
                            <pre>${JSON.stringify(returnData.data, null, 2)}</pre>
                        `;
                        returnsContainer.appendChild(returnDiv);
                    })
                    .catch(error => {
                        console.error(`Error fetching ${year} return:`, error);
                        const returnDiv = document.createElement('div');
                        returnDiv.className = 'return-item error';
                        returnDiv.textContent = `Error loading ${year} tax return: ${error.message}`;
                        returnsContainer.appendChild(returnDiv);
                    });
            });
        })
        .catch(error => {
            console.error('Error fetching account data:', error);
            document.getElementById('error').textContent = `Error: ${error.message}`;
        });
} 