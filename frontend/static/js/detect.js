// Detection Page JavaScript
let selectedFile = null;
let currentResult = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupDragAndDrop();
    setupFileInput();
});

// Drag and Drop functionality
function setupDragAndDrop() {
    const uploadCard = document.getElementById('uploadCard');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadCard.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadCard.addEventListener(eventName, () => {
            uploadCard.classList.add('dragover');
        });
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadCard.addEventListener(eventName, () => {
            uploadCard.classList.remove('dragover');
        });
    });
    
    uploadCard.addEventListener('drop', handleDrop);
    uploadCard.addEventListener('click', () => {
        document.getElementById('imageInput').click();
    });
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// File Input
function setupFileInput() {
    const fileInput = document.getElementById('imageInput');
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });
}

function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please upload an image file (JPG, PNG)');
        return;
    }
    
    if (file.size > 16 * 1024 * 1024) {
        alert('File size must be less than 16MB');
        return;
    }
    
    selectedFile = file;
    showPreview(file);
}

function showPreview(file) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        document.getElementById('previewImage').src = e.target.result;
        document.getElementById('uploadCard').style.display = 'none';
        document.getElementById('previewCard').style.display = 'block';
    };
    
    reader.readAsDataURL(file);
}

function clearImage() {
    selectedFile = null;
    document.getElementById('uploadCard').style.display = 'block';
    document.getElementById('previewCard').style.display = 'none';
    document.getElementById('imageInput').value = '';
    hideResults();
}

// Detect Disease
async function detectDisease() {
    if (!selectedFile) {
        alert('Please select an image first');
        return;
    }
    
    // Show loading
    document.getElementById('previewCard').style.display = 'none';
    document.getElementById('loadingCard').style.display = 'block';
    
    // Prepare form data
    const formData = new FormData();
    formData.append('image', selectedFile);
    
    try {
        const response = await fetch('/api/detect', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Detection failed');
        }
        
        const result = await response.json();
        currentResult = result;
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error detecting disease. Please try again.');
        document.getElementById('loadingCard').style.display = 'none';
        document.getElementById('previewCard').style.display = 'block';
    }
}

function displayResults(result) {
    // Hide loading, show results
    document.getElementById('loadingCard').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';
    
    // Disease name
    const diseaseName = result.disease_name.replace(/___/g, ' - ').replace(/_/g, ' ');
    document.getElementById('diseaseName').textContent = diseaseName;
    
    // Confidence
    document.getElementById('confidenceScore').textContent = result.confidence.toFixed(2) + '%';
    
    // Set confidence badge color
    const confidenceBadge = document.getElementById('confidenceBadge');
    if (result.confidence >= 90) {
        confidenceBadge.style.background = '#ecfdf5';
        confidenceBadge.style.color = '#059669';
    } else if (result.confidence >= 70) {
        confidenceBadge.style.background = '#fef3c7';
        confidenceBadge.style.color = '#d97706';
    } else {
        confidenceBadge.style.background = '#fee2e2';
        confidenceBadge.style.color = '#dc2626';
    }
    
    // Description and symptoms
    document.getElementById('diseaseDescription').textContent = result.disease_info.description;
    document.getElementById('diseaseSymptoms').textContent = result.disease_info.symptoms;
    
    // Severity
    const severityText = result.disease_info.severity;
    document.getElementById('severityValue').textContent = severityText;
    
    const severityValue = document.getElementById('severityValue');
    if (severityText.includes('None') || severityText.includes('Low')) {
        severityValue.className = 'severity-value low';
        document.getElementById('resultIcon').className = 'result-icon';
    } else if (severityText.includes('Medium')) {
        severityValue.className = 'severity-value medium';
        document.getElementById('resultIcon').className = 'result-icon warning';
    } else {
        severityValue.className = 'severity-value high';
        document.getElementById('resultIcon').className = 'result-icon danger';
    }
    
    // Treatment
    const treatmentList = document.getElementById('treatmentList');
    treatmentList.innerHTML = '';
    result.disease_info.treatment.forEach(treatment => {
        const li = document.createElement('li');
        li.textContent = treatment;
        treatmentList.appendChild(li);
    });
    
    // Organic solution
    document.getElementById('organicSolution').textContent = result.disease_info.organic_solution;
    
    // Prevention
    const preventionList = document.getElementById('preventionList');
    preventionList.innerHTML = '';
    result.disease_info.prevention.forEach(prevention => {
        const li = document.createElement('li');
        li.textContent = prevention;
        preventionList.appendChild(li);
    });
}

function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
}

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    if (tabName === 'chemical') {
        document.getElementById('chemicalTab').classList.add('active');
        document.querySelector('.tab-btn:first-child').classList.add('active');
    } else {
        document.getElementById('organicTab').classList.add('active');
        document.querySelector('.tab-btn:last-child').classList.add('active');
    }
}

// Download report
function downloadReport() {
    if (!currentResult) return;
    
    const diseaseName = currentResult.disease_name.replace(/___/g, ' - ').replace(/_/g, ' ');
    const date = new Date().toLocaleDateString();
    
    let report = `CROP DISEASE DETECTION REPORT\n`;
    report += `Generated by CropGuard AI\n`;
    report += `Date: ${date}\n`;
    report += `\n${'='.repeat(50)}\n\n`;
    
    report += `DISEASE IDENTIFIED: ${diseaseName}\n`;
    report += `Confidence Score: ${currentResult.confidence.toFixed(2)}%\n`;
    report += `Severity: ${currentResult.disease_info.severity}\n\n`;
    
    report += `DESCRIPTION:\n${currentResult.disease_info.description}\n\n`;
    report += `SYMPTOMS:\n${currentResult.disease_info.symptoms}\n\n`;
    
    report += `CHEMICAL TREATMENT:\n`;
    currentResult.disease_info.treatment.forEach((t, i) => {
        report += `${i + 1}. ${t}\n`;
    });
    
    report += `\nORGANIC SOLUTION:\n${currentResult.disease_info.organic_solution}\n\n`;
    
    report += `PREVENTION MEASURES:\n`;
    currentResult.disease_info.prevention.forEach((p, i) => {
        report += `${i + 1}. ${p}\n`;
    });
    
    report += `\n${'='.repeat(50)}\n`;
    report += `\nDISCLAIMER:\n`;
    report += `This is an AI-based preliminary diagnosis. Please consult\n`;
    report += `agricultural experts for confirmation and detailed treatment plans.\n`;
    
    // Create download
    const blob = new Blob([report], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `disease_report_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Save to history
async function saveToHistory() {
    alert('Detection saved to your history! View it in your dashboard.');
    // This would integrate with the backend if user is logged in
}
