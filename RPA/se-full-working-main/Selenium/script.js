// Global variables
let currentSection = 'dashboard';
let testResults = [];
let isTestRunning = false;
let currentInstanceId = null;
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadTestData();
});

// Initialize the application
function initializeApp() {
    console.log('Selenium Automation Hub initialized');
    showNotification('Welcome to Selenium Automation Hub!', 'success');
    
    // Initialize charts if Chart.js is available
    if (typeof Chart !== 'undefined') {
        initializeCharts();
    }
    
    // Create initial automation instance
    createAutomationInstance();
    
    // Start polling for status updates
    startStatusPolling();
}

// Setup event listeners
function setupEventListeners() {
    // Navigation
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSection = this.getAttribute('href').substring(1);
            navigateToSection(targetSection);
        });
    });

    // Form inputs
    const formInputs = document.querySelectorAll('.form-input, .form-select, .form-textarea');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });

    // Test options
    const testOptions = document.querySelectorAll('input[name="test-suite"]');
    testOptions.forEach(option => {
        option.addEventListener('change', function() {
            updateTestSelection(this.value);
        });
    });
}

// Navigation functions
function navigateToSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        currentSection = sectionId;
    }

    // Update navigation
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active');
    });

    const activeLink = document.querySelector(`[href="#${sectionId}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
}

// API Helper Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'API call failed');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        showNotification(`API Error: ${error.message}`, 'error');
        throw error;
    }
}

async function createAutomationInstance() {
    try {
        const result = await apiCall('/automation/create', 'POST', {
            instance_id: `instance_${Date.now()}`,
            headless: false
        });
        
        if (result.success) {
            currentInstanceId = result.instance_id || `instance_${Date.now()}`;
            showNotification('Automation instance created successfully', 'success');
        }
    } catch (error) {
        showNotification('Failed to create automation instance', 'error');
    }
}

function startStatusPolling() {
    // Poll for status updates every 5 seconds
    setInterval(async () => {
        try {
            const status = await apiCall('/status');
            updateStatusDisplay(status);
        } catch (error) {
            // Silently handle polling errors
        }
    }, 5000);
}

function updateStatusDisplay(status) {
    // Update dashboard stats with real data
    const statNumbers = document.querySelectorAll('.stat-number');
    if (statNumbers.length >= 4) {
        statNumbers[2].textContent = `${status.active_instances}`;
        statNumbers[3].textContent = `${status.total_results}`;
    }
}

// Quick Action Functions
async function runGoogleSearch() {
    if (!currentInstanceId) {
        showNotification('No automation instance available', 'error');
        return;
    }
    
    showLoading('Running Google Search automation...');
    
    try {
        const result = await apiCall('/search', 'POST', {
            instance_id: currentInstanceId,
            search_engine: 'google',
            query: 'Python Selenium automation'
        });
        
        hideLoading();
        showNotification('Google Search automation completed successfully!', 'success');
        addTestResult('Google Search Test', 'success', 'Search automation completed');
        updateStats();
    } catch (error) {
        hideLoading();
        showNotification('Google Search automation failed', 'error');
    }
}

async function runFormTest() {
    if (!currentInstanceId) {
        showNotification('No automation instance available', 'error');
        return;
    }
    
    showLoading('Running Form automation...');
    
    try {
        const result = await apiCall('/form/fill', 'POST', {
            instance_id: currentInstanceId,
            form_url: 'https://httpbin.org/forms/post',
            form_data: {
                'custname': 'John Doe',
                'custtel': '123-456-7890',
                'custemail': 'john@example.com'
            }
        });
        
        hideLoading();
        showNotification('Form automation completed successfully!', 'success');
        addTestResult('Form Automation', 'success', 'Form filling completed');
        updateStats();
    } catch (error) {
        hideLoading();
        showNotification('Form automation failed', 'error');
    }
}

async function runScreenshot() {
    if (!currentInstanceId) {
        showNotification('No automation instance available', 'error');
        return;
    }
    
    showLoading('Taking screenshot...');
    
    try {
        const result = await apiCall('/screenshot', 'POST', {
            instance_id: currentInstanceId,
            filename: `screenshot_${Date.now()}.png`
        });
        
        hideLoading();
        showNotification('Screenshot captured and saved!', 'success');
        addTestResult('Screenshot Test', 'success', 'Screenshot saved');
        updateStats();
    } catch (error) {
        hideLoading();
        showNotification('Screenshot failed', 'error');
    }
}

async function runDataExtraction() {
    if (!currentInstanceId) {
        showNotification('No automation instance available', 'error');
        return;
    }
    
    showLoading('Extracting data...');
    
    try {
        const result = await apiCall('/extract', 'POST', {
            instance_id: currentInstanceId,
            selectors: {
                'title': 'h1',
                'content': '.content',
                'links': 'a'
            }
        });
        
        hideLoading();
        showNotification('Data extraction completed!', 'success');
        addTestResult('Data Extraction', 'success', 'Data extracted successfully');
        updateStats();
        
        // Log extracted data
        console.log('Extracted Data:', result.data);
    } catch (error) {
        hideLoading();
        showNotification('Data extraction failed', 'error');
    }
}

// Automation Functions
async function navigateToWebsite() {
    if (!currentInstanceId) {
        showNotification('No automation instance available', 'error');
        return;
    }
    
    const url = document.getElementById('url-input').value;
    const headless = document.getElementById('headless-mode').checked;
    
    if (!url) {
        showNotification('Please enter a valid URL', 'error');
        return;
    }
    
    showLoading(`Navigating to ${url}...`);
    
    try {
        const result = await apiCall('/navigate', 'POST', {
            instance_id: currentInstanceId,
            url: url
        });
        
        hideLoading();
        showNotification(`Successfully navigated to ${url}`, 'success');
        addTestResult('Website Navigation', 'success', `Navigated to ${url}`);
        updateStats();
    } catch (error) {
        hideLoading();
        showNotification(`Failed to navigate to ${url}`, 'error');
    }
}

async function performSearch() {
    if (!currentInstanceId) {
        showNotification('No automation instance available', 'error');
        return;
    }
    
    const searchEngine = document.getElementById('search-engine').value;
    const query = document.getElementById('search-query').value;
    
    if (!query) {
        showNotification('Please enter a search query', 'error');
        return;
    }
    
    showLoading(`Performing ${searchEngine} search for "${query}"...`);
    
    try {
        const result = await apiCall('/search', 'POST', {
            instance_id: currentInstanceId,
            search_engine: searchEngine,
            query: query
        });
        
        hideLoading();
        showNotification(`Search completed on ${searchEngine}`, 'success');
        addTestResult('Search Automation', 'success', `${searchEngine} search for "${query}"`);
        updateStats();
    } catch (error) {
        hideLoading();
        showNotification(`Search failed on ${searchEngine}`, 'error');
    }
}

async function fillForm() {
    if (!currentInstanceId) {
        showNotification('No automation instance available', 'error');
        return;
    }
    
    const formUrl = document.getElementById('form-url').value;
    const formData = document.getElementById('form-data').value;
    
    if (!formUrl || !formData) {
        showNotification('Please provide both form URL and data', 'error');
        return;
    }
    
    try {
        const parsedData = JSON.parse(formData); // Validate JSON
        
        showLoading('Filling form with provided data...');
        
        const result = await apiCall('/form/fill', 'POST', {
            instance_id: currentInstanceId,
            form_url: formUrl,
            form_data: parsedData
        });
        
        hideLoading();
        showNotification('Form filled successfully!', 'success');
        addTestResult('Form Filling', 'success', 'Form data submitted');
        updateStats();
    } catch (e) {
        if (e.message.includes('API Error')) {
            hideLoading();
            showNotification('Form filling failed', 'error');
        } else {
            showNotification('Please provide valid JSON data', 'error');
        }
    }
}

async function extractData() {
    if (!currentInstanceId) {
        showNotification('No automation instance available', 'error');
        return;
    }
    
    const selectors = document.getElementById('extraction-selectors').value;
    
    if (!selectors) {
        showNotification('Please provide CSS selectors', 'error');
        return;
    }
    
    try {
        const parsedSelectors = JSON.parse(selectors); // Validate JSON
        
        showLoading('Extracting data from page...');
        
        const result = await apiCall('/extract', 'POST', {
            instance_id: currentInstanceId,
            selectors: parsedSelectors
        });
        
        hideLoading();
        showNotification('Data extracted successfully!', 'success');
        addTestResult('Data Extraction', 'success', 'Data extracted from page');
        updateStats();
        
        // Show extracted data
        console.log('Extracted Data:', result.data);
    } catch (e) {
        if (e.message.includes('API Error')) {
            hideLoading();
            showNotification('Data extraction failed', 'error');
        } else {
            showNotification('Please provide valid JSON selectors', 'error');
        }
    }
}

// Testing Functions
async function runTestSuite() {
    if (isTestRunning) {
        showNotification('Tests are already running', 'warning');
        return;
    }
    
    const selectedSuite = document.querySelector('input[name="test-suite"]:checked').value;
    isTestRunning = true;
    
    showLoading(`Running ${selectedSuite} test suite...`);
    clearTestOutput();
    addTestMessage('info', `Starting ${selectedSuite} test suite...`);
    
    try {
        const result = await apiCall('/tests/run', 'POST', {
            test_suite: selectedSuite
        });
        
        if (result.success) {
            addTestMessage('info', `${selectedSuite} test suite started successfully`);
            
            // Poll for test completion
            const pollInterval = setInterval(async () => {
                try {
                    const status = await apiCall('/status');
                    if (!status.is_running) {
                        clearInterval(pollInterval);
                        isTestRunning = false;
                        hideLoading();
                        addTestMessage('info', 'Test suite completed!');
                        showNotification(`${selectedSuite} test suite completed`, 'success');
                        updateStats();
                        loadResults();
                    }
                } catch (error) {
                    clearInterval(pollInterval);
                    isTestRunning = false;
                    hideLoading();
                    addTestMessage('error', 'Error checking test status');
                }
            }, 2000);
        }
    } catch (error) {
        isTestRunning = false;
        hideLoading();
        addTestMessage('error', `Failed to start test suite: ${error.message}`);
        showNotification('Failed to start test suite', 'error');
    }
}

async function stopTests() {
    if (!isTestRunning) {
        showNotification('No tests are currently running', 'warning');
        return;
    }
    
    try {
        const result = await apiCall('/tests/stop', 'POST');
        isTestRunning = false;
        hideLoading();
        addTestMessage('warning', 'Tests stopped by user');
        showNotification('Tests stopped', 'warning');
    } catch (error) {
        showNotification('Failed to stop tests', 'error');
    }
}

async function generateReport() {
    showLoading('Generating test report...');
    
    try {
        const result = await apiCall('/results/export/json');
        
        hideLoading();
        showNotification('Test report generated successfully!', 'success');
        
        // Download report
        downloadReport(result);
    } catch (error) {
        hideLoading();
        showNotification('Failed to generate report', 'error');
    }
}

// Utility Functions
function showLoading(message = 'Processing...') {
    const overlay = document.getElementById('loading-overlay');
    const spinner = overlay.querySelector('p');
    spinner.textContent = message;
    overlay.classList.add('active');
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    overlay.classList.remove('active');
}

function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    container.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success': return 'check-circle';
        case 'error': return 'times-circle';
        case 'warning': return 'exclamation-triangle';
        default: return 'info-circle';
    }
}

function addTestResult(name, status, description) {
    const result = {
        name,
        status,
        description,
        timestamp: new Date().toISOString()
    };
    
    testResults.unshift(result);
    
    // Update recent results display
    updateRecentResults();
}

function addTestMessage(type, message) {
    const output = document.getElementById('test-output');
    const messageDiv = document.createElement('div');
    messageDiv.className = `test-message ${type}`;
    messageDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    output.appendChild(messageDiv);
    output.scrollTop = output.scrollHeight;
}

function clearTestOutput() {
    const output = document.getElementById('test-output');
    output.innerHTML = '';
}

function updateRecentResults() {
    const container = document.getElementById('recent-results');
    container.innerHTML = '';
    
    testResults.slice(0, 5).forEach(result => {
        const resultDiv = document.createElement('div');
        resultDiv.className = `result-item ${result.status}`;
        resultDiv.innerHTML = `
            <i class="fas fa-${result.status === 'success' ? 'check-circle' : 'times-circle'}"></i>
            <span>${result.name} - ${result.status === 'success' ? 'Passed' : 'Failed'}</span>
            <span class="result-time">${formatTimeAgo(result.timestamp)}</span>
        `;
        container.appendChild(resultDiv);
    });
}

function updateStats() {
    // Update dashboard stats
    const totalTests = testResults.length;
    const passedTests = testResults.filter(r => r.status === 'success').length;
    const successRate = totalTests > 0 ? Math.round((passedTests / totalTests) * 100) : 0;
    
    // Update stat numbers (you can make these dynamic)
    const statNumbers = document.querySelectorAll('.stat-number');
    if (statNumbers.length >= 4) {
        statNumbers[1].textContent = `${successRate}%`;
        statNumbers[3].textContent = totalTests;
    }
}

function getTestSuite(suiteType) {
    const suites = {
        basic: [
            { name: 'Google Search Test', description: 'Basic search functionality' },
            { name: 'Form Validation Test', description: 'Form input validation' },
            { name: 'Navigation Test', description: 'Website navigation' }
        ],
        advanced: [
            { name: 'Data Extraction Test', description: 'Complex data extraction' },
            { name: 'Screenshot Test', description: 'Page screenshot capture' },
            { name: 'Performance Test', description: 'Page load performance' },
            { name: 'Cross-browser Test', description: 'Multi-browser compatibility' }
        ],
        custom: [
            { name: 'Custom Test 1', description: 'User-defined test case' },
            { name: 'Custom Test 2', description: 'User-defined test case' },
            { name: 'Custom Test 3', description: 'User-defined test case' }
        ]
    };
    
    return suites[suiteType] || suites.basic;
}

function updateTestSelection(suiteType) {
    console.log(`Selected test suite: ${suiteType}`);
}

function formatTimeAgo(timestamp) {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInMinutes = Math.floor((now - time) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes} min ago`;
    
    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24) return `${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`;
    
    const diffInDays = Math.floor(diffInHours / 24);
    return `${diffInDays} day${diffInDays > 1 ? 's' : ''} ago`;
}

async function loadTestData() {
    try {
        const result = await apiCall('/results');
        testResults = result.results || [];
        updateRecentResults();
        updateStats();
    } catch (error) {
        // Load sample test data if API fails
        const sampleResults = [
            { name: 'Google Search Test', status: 'success', description: 'Search automation completed', timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString() },
            { name: 'Form Automation', status: 'error', description: 'Form submission failed', timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString() },
            { name: 'Data Extraction', status: 'success', description: 'Data extracted successfully', timestamp: new Date(Date.now() - 10 * 60 * 1000).toISOString() }
        ];
        
        testResults = sampleResults;
        updateRecentResults();
        updateStats();
    }
}

async function loadResults() {
    try {
        const result = await apiCall('/results');
        testResults = result.results || [];
        updateRecentResults();
        updateStats();
    } catch (error) {
        console.error('Failed to load results:', error);
    }
}

function downloadReport(report) {
    const dataStr = JSON.stringify(report, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `test-report-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
}

// Export Functions
async function exportResults(format) {
    showLoading(`Exporting results as ${format.toUpperCase()}...`);
    
    try {
        const response = await fetch(`${API_BASE_URL}/results/export/${format}`);
        
        if (!response.ok) {
            throw new Error('Export failed');
        }
        
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `selenium-results-${new Date().toISOString().split('T')[0]}.${format}`;
        link.click();
        URL.revokeObjectURL(url);
        
        hideLoading();
        showNotification(`Results exported as ${format.toUpperCase()}`, 'success');
    } catch (error) {
        hideLoading();
        showNotification(`Failed to export results as ${format.toUpperCase()}`, 'error');
    }
}

function convertToCSV(data) {
    const headers = ['Name', 'Status', 'Description', 'Timestamp'];
    const rows = data.results.map(r => [r.name, r.status, r.description, r.timestamp]);
    return [headers, ...rows].map(row => row.join(',')).join('\n');
}

function convertToHTML(data) {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Selenium Test Results</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .success { color: green; }
                .error { color: red; }
            </style>
        </head>
        <body>
            <h1>Selenium Test Results</h1>
            <p>Generated: ${data.timestamp}</p>
            <p>Total: ${data.summary.total} | Passed: ${data.summary.passed} | Failed: ${data.summary.failed}</p>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Status</th>
                    <th>Description</th>
                    <th>Timestamp</th>
                </tr>
                ${data.results.map(r => `
                    <tr>
                        <td>${r.name}</td>
                        <td class="${r.status}">${r.status}</td>
                        <td>${r.description}</td>
                        <td>${r.timestamp}</td>
                    </tr>
                `).join('')}
            </table>
        </body>
        </html>
    `;
}

// Footer Functions
function showHelp() {
    showNotification('Help documentation will be available soon!', 'info');
}

function showAbout() {
    showNotification('Selenium Automation Hub v1.0 - Built for web automation', 'info');
}

function showSettings() {
    showNotification('Settings panel will be available soon!', 'info');
}

// Chart initialization (if Chart.js is available)
function initializeCharts() {
    const ctx = document.getElementById('performanceChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Passed', 'Failed', 'Pending'],
                datasets: [{
                    data: [75, 15, 10],
                    backgroundColor: ['#28a745', '#dc3545', '#ffc107'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    }
                }
            }
        });
    }
}

// Add slideOut animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style); 