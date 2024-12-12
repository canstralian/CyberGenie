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

        fetch('/scans/new', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = `/scans/${data.scan_id}`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while starting the scan');
        });
    });
});
