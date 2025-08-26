function showForm(domain) {
    document.getElementById('main-menu').classList.remove('visible');
    document.getElementById('main-menu').classList.add('hidden');
    
    if (domain === 'finance') {
        document.getElementById('finance-form').classList.remove('hidden');
        document.getElementById('finance-form').classList.add('visible');
    } else {
        document.getElementById('health-form').classList.remove('hidden');
        document.getElementById('health-form').classList.add('visible');
    }
}

function backToMenu() {
    document.getElementById('finance-form').classList.remove('visible');
    document.getElementById('finance-form').classList.add('hidden');
    document.getElementById('health-form').classList.remove('visible');
    document.getElementById('health-form').classList.add('hidden');
    document.getElementById('analysis-preview').classList.remove('visible');
    document.getElementById('analysis-preview').classList.add('hidden');
    
    document.getElementById('main-menu').classList.remove('hidden');
    document.getElementById('main-menu').classList.add('visible');
}

function submitForm(event, domain) {
    event.preventDefault();
    const formData = {};
    const form = document.getElementById(domain + 'Form');
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        let key = input.id;
        if (key.startsWith('h_')) key = key.substring(2);
        formData[key] = input.value;
    });

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalContent = submitBtn.innerHTML;
    submitBtn.innerHTML = '<div class="loading-animation"></div> Analyzing...';
    submitBtn.disabled = true;

    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ domain: domain, data: formData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            // Hide form and show analysis preview
            form.classList.remove('visible');
            form.classList.add('hidden');
            document.getElementById('analysis-preview').classList.remove('hidden');
            document.getElementById('analysis-preview').classList.add('visible');

            // Display the analysis text
            document.getElementById('analysis-content').innerText = data.analysis;

            // Set the download link for the PDF
            document.getElementById('download-pdf-btn').href = data.pdf_link;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during analysis. Please try again.');
    })
    .finally(() => {
        submitBtn.innerHTML = originalContent;
        submitBtn.disabled = false;
    });
}

// Animate cards on load
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.analyzer-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s cubic-bezier(0.4,0,0.2,1)';
        
        setTimeout(() => { 
            card.style.opacity = '1'; 
            card.style.transform = 'translateY(0)'; 
        }, index * 200 + 100);
    });
});