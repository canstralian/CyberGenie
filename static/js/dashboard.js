document.addEventListener('DOMContentLoaded', function() {
    // Initialize vulnerability chart
    const ctx = document.getElementById('vulnerabilityChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Critical', 'High', 'Medium', 'Low'],
            datasets: [{
                data: [4, 8, 15, 16],
                backgroundColor: [
                    'var(--bs-danger)',
                    'var(--bs-warning)',
                    'var(--bs-info)',
                    'var(--bs-success)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Handle new scan form submission
    document.getElementById('startScan').addEventListener('click', function() {
        const form = document.getElementById('newScanForm');
        const formData = new FormData(form);

        // Validate form fields
        if (!validateForm(form)) {
            alert('Please fill out all required fields.');
            return; // Prevent submission if validation fails
        }

        // Disable the 'startScan' button and show a loading indicator
        const startScanButton = document.getElementById('startScan');
        startScanButton.disabled = true;
        startScanButton.innerHTML = 'Starting Scan...';

        // Show loading spinner
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'inline-block';
        }

        // Submit the form data
        fetch('/scans/new', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = `/scans/${data.scan_id}`;
            } else {
                alert('Failed to start scan: ' + data.message);
                startScanButton.disabled = false;
                startScanButton.innerHTML = 'Start Scan';
                if (loadingIndicator) {
                    loadingIndicator.style.display = 'none';
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while starting the scan.');
            startScanButton.disabled = false;
            startScanButton.innerHTML = 'Start Scan';
            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
        });
    });

    // Form validation function
    function validateForm(form) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('is-invalid'); // Add Bootstrap invalid class for styling
                field.addEventListener('input', function() {
                    field.classList.remove('is-invalid'); // Remove invalid class when user starts typing
                });
            } else {
                field.classList.remove('is-invalid');
            }
        });

        return isValid;
    }
});