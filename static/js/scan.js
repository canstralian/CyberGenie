document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();

    // Handle severity filtering
    initializeSeverityFilter();

    // Initialize severity chart if we're on the detail page
    initializeSeverityChart();

    // Handle new scan form submission
    initializeScanForm();

    // Handle scan status updates for running scans
    initializeScanStatus();
});

// Helper function to initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

// Helper function to handle severity filter
function initializeSeverityFilter() {
    const severityFilter = document.getElementById('severityFilter');
    if (severityFilter) {
        severityFilter.addEventListener('change', function() {
            const selected = this.value;
            const findings = document.querySelectorAll('.finding-card');
            
            findings.forEach(finding => {
                finding.style.display = (!selected || finding.dataset.severity === selected) ? 'block' : 'none';
            });
        });
    }
}

// Helper function to initialize the severity chart
function initializeSeverityChart() {
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
}

// Helper function to handle new scan form submission
function initializeScanForm() {
    const startScanBtn = document.getElementById('startScan');
    if (startScanBtn) {
        startScanBtn.addEventListener('click', function() {
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
    }
}

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

// Helper function to submit scan form
function submitScanForm(formData) {
    fetch('/scans/new', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            window.location.href = `/scans/${data.scan_id}`;
        } else {
            alert(`Scan failed: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while starting the scan');
    });
}

// Helper function to handle scan status updates
function initializeScanStatus() {
    const scanStatusToast = document.getElementById('scanStatusToast');
    if (scanStatusToast) {
        const toast = new bootstrap.Toast(scanStatusToast);
        toast.show();

        const scanId = window.location.pathname.split('/').pop();
        pollScanStatus(scanId);
    }
}

// Helper function to poll scan status updates
function pollScanStatus(scanId) {
    const statusCheck = setInterval(() => {
        fetch(`/scans/${scanId}/status`)
            .then(response => response.json())
            .then(data => {
                updateScanProgress(data);
                if (data.status === 'completed' || data.status === 'failed') {
                    clearInterval(statusCheck);
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                clearInterval(statusCheck);
                alert('An error occurred while checking scan status');
            });
    }, 10000); // Adjusted interval to 10 seconds for fewer API calls
}

// Helper function to update the scan progress display
function updateScanProgress(data) {
    const progressElement = document.getElementById('scanProgress');
    if (progressElement) {
        progressElement.textContent = data.progress;
    }
}

// Helper function to calculate severity counts for the chart
function calculateSeverityCounts() {
    const findings = document.querySelectorAll('.finding-card');
    const counts = { critical: 0, high: 0, medium: 0, low: 0 };

    findings.forEach(finding => {
        const severity = finding.dataset.severity;
        if (counts[severity] !== undefined) {
            counts[severity]++;
        }
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
