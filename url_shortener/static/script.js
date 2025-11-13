const API_BASE = window.location.origin;

// DOM Elements
const shortenForm = document.getElementById('shortenForm');
const urlInput = document.getElementById('urlInput');
const customCode = document.getElementById('customCode');
const shortenBtn = document.getElementById('shortenBtn');
const btnText = document.querySelector('.btn-text');
const loader = document.querySelector('.loader');
const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');
const shortUrlInput = document.getElementById('shortUrl');
const copyBtn = document.getElementById('copyBtn');
const originalUrlSpan = document.getElementById('originalUrl');
const clicksSpan = document.getElementById('clicks');
const createdAtSpan = document.getElementById('createdAt');
const newUrlBtn = document.getElementById('newUrlBtn');
const recentList = document.getElementById('recentList');

// Event Listeners
shortenForm.addEventListener('submit', handleSubmit);
copyBtn.addEventListener('click', copyToClipboard);
newUrlBtn.addEventListener('click', resetForm);

// Load recent URLs on page load
loadRecentUrls();

async function handleSubmit(e) {
    e.preventDefault();
    
    const url = urlInput.value.trim();
    const custom = customCode.value.trim();
    
    if (!url) {
        showError('Please enter a URL');
        return;
    }
    
    // Show loading state
    setLoading(true);
    hideError();
    hideResult();
    
    try {
        const response = await fetch(`${API_BASE}/api/shorten`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                custom_code: custom
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to shorten URL');
        }
        
        // Show result
        displayResult(data);
        
        // Reload recent URLs
        loadRecentUrls();
        
    } catch (error) {
        showError(error.message);
    } finally {
        setLoading(false);
    }
}

function displayResult(data) {
    shortUrlInput.value = data.short_url;
    originalUrlSpan.textContent = data.original_url;
    clicksSpan.textContent = data.clicks;
    createdAtSpan.textContent = formatDate(data.created_at);
    
    resultDiv.style.display = 'block';
    shortenForm.style.display = 'none';
}

function copyToClipboard() {
    shortUrlInput.select();
    document.execCommand('copy');
    
    const originalText = copyBtn.textContent;
    copyBtn.textContent = 'Copied!';
    copyBtn.classList.add('copied');
    
    setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.classList.remove('copied');
    }, 2000);
}

function resetForm() {
    shortenForm.reset();
    shortenForm.style.display = 'block';
    resultDiv.style.display = 'none';
    hideError();
}

function setLoading(isLoading) {
    shortenBtn.disabled = isLoading;
    if (isLoading) {
        btnText.style.display = 'none';
        loader.style.display = 'block';
    } else {
        btnText.style.display = 'block';
        loader.style.display = 'none';
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorDiv.style.display = 'block';
}

function hideError() {
    errorDiv.style.display = 'none';
}

function hideResult() {
    resultDiv.style.display = 'none';
}

async function loadRecentUrls() {
    try {
        const response = await fetch(`${API_BASE}/api/recent?limit=5`);
        const urls = await response.json();
        
        if (urls.length === 0) {
            recentList.innerHTML = '<p class="loading">No URLs yet. Create your first short URL!</p>';
            return;
        }
        
        recentList.innerHTML = urls.map(url => `
            <div class="recent-item">
                <div class="recent-item-header">
                    <span class="recent-item-code">/${url.short_code}</span>
                    <span class="recent-item-clicks">👁️ ${url.clicks} clicks</span>
                </div>
                <div class="recent-item-url">${truncateUrl(url.original_url, 60)}</div>
                <div class="recent-item-date">${formatDate(url.created_at)}</div>
            </div>
        `).join('');
        
    } catch (error) {
        recentList.innerHTML = '<p class="loading">Failed to load recent URLs</p>';
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

function truncateUrl(url, maxLength) {
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
}

// Auto-refresh recent URLs every 30 seconds
setInterval(loadRecentUrls, 30000);
