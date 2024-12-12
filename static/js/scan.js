document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Handle severity filtering
    const severityFilter = document.getElementById('severityFilter');
    if (severityFilter) {
        severityFilter.addEventListener('change', function() {
            const selected = this.value;
            const findings = document.querySelectorAll('.finding-card');
            
            findings.forEach(finding => {
                if (!selected || finding.dataset.severity === selected) {
                    finding.style.display = 'block';
                } else {
                    finding.style.display = 'none';
                }
            });
        });
    }

    // Initialize severity chart if we're on the detail page
    const chartCanvas = document.getElementById('severityChart');
    if (chartCanvas) {
        new Chart(chartCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Critical', 'High', 'Medium', 'Low'],
                datasets: [{
                    data: calculateSeverityCounts(),
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
    }

    // Handle new scan form submission
    const startScanBtn = document.getElementById('startScan');
    if (startScanBtn) {
        startScanBtn.addEventListener('click', function() {
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
    }

    // Handle scan status updates for running scans
    const scanStatusToast = document.getElementById('scanStatusToast');
    if (scanStatusToast) {
        const toast = new bootstrap.Toast(scanStatusToast);
        toast.show();

        // Poll for scan status updates
        const scanId = window.location.pathname.split('/').pop();
        const statusCheck = setInterval(() => {
            fetch(`/scans/${scanId}/status`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('scanProgress').textContent = data.progress;
                    if (data.status === 'completed' || data.status === 'failed') {
                        clearInterval(statusCheck);
                        window.location.reload();
                    }
                });
        }, 5000);
    }
});

// Helper function to calculate severity counts for the chart
function calculateSeverityCounts() {
    const findings = document.querySelectorAll('.finding-card');
    const counts = {
        critical: 0,
        high: 0,
        medium: 0,
        low: 0
    };
    
    findings.forEach(finding => {
        const severity = finding.dataset.severity;
        counts[severity]++;
    });
    
    return [counts.critical, counts.high, counts.medium, counts.low];
}

// Handle report download
function downloadReport(scanId) {
    fetch(`/scans/${scanId}/report`)
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `scan_report_${scanId}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while downloading the report');
        });
}
