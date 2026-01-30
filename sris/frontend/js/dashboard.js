const API_BASE = window.location.origin.includes('127.0.0.1') || window.location.origin.includes('localhost')
    ? "http://127.0.0.1:8000/api"
    : "/api";

async function fetchSummary() {
    try {
        const response = await fetch(`${API_BASE}/data/summary`);
        const data = await response.json();
        document.getElementById('salesCount').innerText = data.sales_records.toLocaleString();
        document.getElementById('customerCount').innerText = data.customers.toLocaleString();
        document.getElementById('productCount').innerText = data.products.toLocaleString();
    } catch (error) {
        console.error('Error fetching summary:', error);
    }
}

async function trainModels() {
    const btnText = document.getElementById('trainBtnText');
    const token = localStorage.getItem('sris_token');

    btnText.innerText = "Training Engine...";
    try {
        const response = await fetch(`${API_BASE}/ml/train-all`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        alert(data.message);
    } catch (err) {
        alert('Training failed');
    } finally {
        btnText.innerText = "Retrain Intelligence Engine";
    }
}

function initCharts() {
    const ctx1 = document.getElementById('revenueChart').getContext('2d');
    new Chart(ctx1, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Monthly Revenue ($)',
                data: [12000, 19000, 15000, 25000, 22000, 30000],
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
            }
        }
    });

    const ctx2 = document.getElementById('categoryChart').getContext('2d');
    new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: ['Electronics', 'Clothing', 'Home', 'Groceries', 'Beauty'],
            datasets: [{
                data: [35, 25, 15, 15, 10],
                backgroundColor: ['#6366f1', '#10b981', '#f59e0b', '#ec4899', '#3b82f6'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } }
        }
    });
}

const uploadForm = document.getElementById('uploadForm');
if (uploadForm) {
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById('csvFile');
        if (!fileInput.files[0]) return;

        const submitBtn = e.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerText;
        submitBtn.disabled = true;
        submitBtn.innerText = 'Processing...';

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        const token = localStorage.getItem('sris_token');

        try {
            const response = await fetch(`${API_BASE}/data/upload-csv`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });

            const result = await response.json().catch(() => ({}));
            if (response.ok && !result.error) {
                alert(result.message || 'Data processed successfully');
                fetchSummary();
                fileInput.value = ''; // Clear selection
            } else {
                alert(`Upload failed: ${result.error || 'Unknown server error'}`);
            }
        } catch (error) {
            console.error('Upload error:', error);
            alert('Upload error. Check console.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerText = originalText;
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    fetchSummary();
    initCharts();
});
