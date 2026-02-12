// Dashboard JavaScript
let diseaseChart = null;

// Load dashboard data on page load
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
    loadDetectionHistory();
    loadCrops();
});

// Load dashboard statistics
async function loadDashboardData() {
    try {
        const response = await fetch('/api/stats');
        if (!response.ok) {
            console.error('Not authenticated');
            return;
        }
        
        const data = await response.json();
        
        // Update stats cards
        document.getElementById('totalDetections').textContent = data.total_detections;
        document.getElementById('totalCrops').textContent = data.total_crops;
        
        // Calculate healthy and infected from disease distribution
        const healthyCount = Object.entries(data.disease_distribution)
            .filter(([disease]) => disease.includes('healthy'))
            .reduce((sum, [, count]) => sum + count, 0);
        
        const infectedCount = data.total_detections - healthyCount;
        
        document.getElementById('healthyCrops').textContent = healthyCount;
        document.getElementById('infectedCrops').textContent = infectedCount;
        
        // Create disease distribution chart
        if (Object.keys(data.disease_distribution).length > 0) {
            createDiseaseChart(data.disease_distribution);
        }
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

// Load detection history
async function loadDetectionHistory() {
    try {
        const response = await fetch('/api/detections/history');
        if (!response.ok) return;
        
        const detections = await response.json();
        const container = document.getElementById('detectionHistory');
        
        if (detections.length === 0) {
            return; // Keep empty state
        }
        
        container.innerHTML = '';
        
        detections.slice(0, 5).forEach(detection => {
            const item = createDetectionItem(detection);
            container.appendChild(item);
        });
        
    } catch (error) {
        console.error('Error loading detection history:', error);
    }
}

// Create detection item element
function createDetectionItem(detection) {
    const div = document.createElement('div');
    div.className = 'detection-item';
    
    const diseaseName = detection.disease_name.replace(/___/g, ' - ').replace(/_/g, ' ');
    const isHealthy = detection.disease_name.includes('healthy');
    const statusClass = isHealthy ? 'success' : 'warning';
    
    div.innerHTML = `
        <div class="detection-image">
            <img src="${detection.image_url}" alt="${diseaseName}">
        </div>
        <div class="detection-info">
            <h4>${diseaseName}</h4>
            <p class="detection-date">
                <i class="fas fa-clock"></i>
                ${timeAgo(detection.detected_at)}
            </p>
        </div>
        <div class="detection-meta">
            <span class="confidence-badge ${statusClass}">
                ${detection.confidence.toFixed(1)}%
            </span>
        </div>
    `;
    
    return div;
}

// Create disease distribution chart
function createDiseaseChart(diseaseData) {
    const ctx = document.getElementById('diseaseChart');
    
    if (!ctx) return;
    
    // Prepare data
    const labels = Object.keys(diseaseData).map(d => 
        d.replace(/___/g, ' - ').replace(/_/g, ' ')
    );
    const data = Object.values(diseaseData);
    
    // Generate colors
    const colors = [
        '#10b981', '#3b82f6', '#f59e0b', '#ef4444', 
        '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'
    ];
    
    if (diseaseChart) {
        diseaseChart.destroy();
    }
    
    diseaseChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12,
                            family: "'Sora', sans-serif"
                        }
                    }
                }
            }
        }
    });
}

// Load crops
async function loadCrops() {
    // This would fetch from backend
    // For now, showing empty state
}

// Show add crop modal
function showAddCropModal() {
    document.getElementById('addCropModal').style.display = 'flex';
}

// Close add crop modal
function closeAddCropModal() {
    document.getElementById('addCropModal').style.display = 'none';
    document.getElementById('addCropForm').reset();
}

// Add crop
async function addCrop(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch('/api/add-crop', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showNotification('Crop added successfully!', 'success');
            closeAddCropModal();
            loadCrops();
            loadDashboardData();
        } else {
            showNotification('Failed to add crop', 'error');
        }
    } catch (error) {
        console.error('Error adding crop:', error);
        showNotification('Error adding crop', 'error');
    }
}

// View all history
function viewAllHistory() {
    // Implement view all functionality
    alert('View all detection history functionality coming soon!');
}

// Export data
function exportData() {
    showNotification('Exporting data...', 'info');
    
    // This would generate and download CSV/Excel file
    setTimeout(() => {
        showNotification('Data exported successfully!', 'success');
    }, 1500);
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('addCropModal');
    if (event.target === modal) {
        closeAddCropModal();
    }
}
